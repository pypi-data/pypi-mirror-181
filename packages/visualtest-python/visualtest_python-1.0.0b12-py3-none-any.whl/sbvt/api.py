import os
import logging
import json
import time
import requests
import atexit
import sbvt
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dotenv import load_dotenv
from colorama import Fore, Style

load_dotenv()

log = logging.getLogger(f'vt.{os.path.basename(__file__)}')
host = os.environ["VT_API_HOST"] if "VT_API_HOST" in os.environ else 'https://api.visualtest.io'
if host == "https://api.dev.visualtest.io":
    cdnUrl = "https://cdn.dev.visualtest.io/browser-toolkit"
elif host == "https://api.int.visualtest.io":
    cdnUrl = "https://cdn.int.visualtest.io/browser-toolkit"
else:
    cdnUrl = "https://cdn.visualtest.io/browser-toolkit"
api = requests.Session()
s3 = requests.Session()


# from https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = 10  # seconds
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


# define retry strategy and timeout
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = TimeoutHTTPAdapter(timeout=10, max_retries=retries)

# Mount it for both http and https usage
api.mount("https://", adapter)
api.mount("http://", adapter)
s3.mount("https://", adapter)

s3.headers.update({"Content-Type": "application/octet-stream"})

class Api:

    baseUrl = f'{host}/api/v1'
    testRuns = []

    def __init__(self, projectToken=None):
        self.projectToken = None
        self.projectId = None
        if projectToken:
            self.projectToken = projectToken
            self.projectId = projectToken.split("/")[0]
            api.headers.update({'Authorization': f'Bearer {projectToken}'})
        self.testRun = None

    def getDeviceInfo(self, userAgentInfo, driverCapabilities):

        url = f'{Api.baseUrl}/device-info/'
        log.info(f'calling API to get device info at: {url}')
        response = api.post(url, json={'userAgentInfo': userAgentInfo, 'driverCapabilities': driverCapabilities})
        if response.status_code in range(200, 300):

            return response.json()
        else:
            raise Exception(f'Failed to save image. HTTP Response: {response}')

    def findTestRunByName(self, name):
        query = {'testRunName': {'eq': name}}
        url = f'{Api.baseUrl}/projects/{self.projectId}/testruns?q={requests.utils.quote(json.dumps(query))}'
        log.info(f'calling API to get testRun by name: {url}')
        response = api.get(url)
        log.info(f'findTestRunByName response: {response}')
        if response.status_code in range(200, 300):
            result = response.json()
            if type(result['items']) == 'list' and len(result['items']) == 1:
                log.info(f'Found existing testRunName: {str(result)}')
                return result['testruns'][0]
            else:
                log.info(f"type of items: {type(result['items'])}")
                log.info(f"length of items: {len(result['items'])}")
                log.info(f'Did NOT find existing testRunName')
                return None
        else:
            raise Exception(f'Failed to get test run by name: {name}. HTTP Response: {str(response)}')

    def createTestRun(self, testRunName):

        url = f'{Api.baseUrl}/projects/{self.projectId}/testruns'
        log.info(f'calling API to create testRun by name: {url}')
        response = api.post(url, json={
            'testRunName': testRunName,
            'sdk': 'python',
            'sdkVersion': sbvt.__version__,
        })
        if response.status_code in range(200, 300):
            return response.json()
        else:
            log.error(f'Failed to create testRun. HTTP Response: {response.json()}')
            raise Exception(f'Failed to create testRun. HTTP Response: {response.json()}')

    def saveImage(self, testRunName, imageData, filePath):
        log.info(f'Saving image for testRunName: {testRunName}')

        # TODO add this logic later with a flag
        # check if testRun already exists, if not create one
        if not self.testRun:
            self.testRun = self.createTestRun(testRunName)
            Api.testRuns.append({"projectId": self.projectId, "testRunId": self.testRun["testRunId"] })

        url = f'{Api.baseUrl}/projects/{self.projectId}/testruns/{self.testRun["testRunId"]}/images'
        log.info(f'calling API to save image: {url}')
        log.debug(f'imageData: {imageData}')

        response = api.post(url, json=imageData)
        log.info(f'create image response: {response}')

        if response.status_code in range(200, 300):
            result = response.json()
        else:
            log.error(f'Failed to create image. HTTP Response: {response.json()}')
            raise Exception(f'Failed to create image. HTTP Response: {response.json()}')

        imageBinary = open(filePath, "rb")
        log.info(f'uploading image to: {result["uploadUrl"]}')

        response = s3.put(result['uploadUrl'], data=imageBinary)
        log.info(f'upload image response: {response}')
        imageBinary.close()

        if response.status_code in range(200, 300):
            return result
        else:
            log.error(f'Failed to upload image. HTTP Response: {response.json()}')
            raise Exception(f'Failed to upload image. HTTP Response: {response.json()}')

    @staticmethod
    def getToolkit(script=None):
        global url
        if script == 'userAgent':
            url = f'{cdnUrl}/user-agent.min.js'
            response = api.get(url)
            return response.text
        elif script == 'domCapture':
            url = f'{cdnUrl}/dom-capture.min.js'
            response = api.get(url)
            return response.text
        else:
            log.error(f'Failed to grab the {script} CDN image.')
            raise Exception(f'Failed to grab the {script} CDN image.')

    @staticmethod
    def printReport():

        for testRun in Api.testRuns:
            if not testRun["testRunId"]:  # logic to check if the users tests failed before a 'saveImage'
                continue

            url = f'{Api.baseUrl}/projects/{testRun["projectId"]}/testruns/{testRun["testRunId"]}/images'
            response = api.get(url).json()
            imageCount = response["page"]["totalItems"]
            print(f'View your {imageCount} {"capture" if imageCount == 1 else "captures"} here: ' + Fore.BLUE + f'https://app.visualtest.io/projects/{response["items"][0]["projectId"]}/testruns/{response["items"][0]["testRunId"]}/comparisons'+ Style.RESET_ALL)

            comparisonUrl = f'{Api.baseUrl}/projects/{testRun["projectId"]}/testruns/{testRun["testRunId"]}?expand=comparison-totals'
            comparisons = {"total": 0}
            maxLoops = 20
            countLoops = 0
            while comparisons["total"] != imageCount and countLoops <= maxLoops:
                time.sleep(0.25)
                log.info(f'imageCount: {imageCount} != comparisonTotal: {comparisons["total"]} -- mismatch... running again for testRun {testRun} countLoops: {countLoops}')
                comparisonResult = api.get(comparisonUrl).json()
                comparisons = comparisonResult["comparisons"]
                countLoops += 1

            if comparisons["new_image"]:
                print(Style.BRIGHT + Fore.YELLOW + f'\t{comparisons["new_image"]} new base {"image" if comparisons["new_image"] == 1 else "images"}' + Style.RESET_ALL)
            if comparisons["failed"]:
                print(Style.BRIGHT + Fore.RED + f'\t{comparisons["failed"]} image comparison {"failure" if comparisons["failed"] == 1 else "failures"} to review' + Style.RESET_ALL)
            if comparisons["passed"]:
                print(Style.RESET_ALL + Style.BRIGHT + Fore.GREEN + f'\t{comparisons["passed"]} image comparisons passed' + Style.RESET_ALL)
            if comparisons["total"] != imageCount:
                print(Style.BRIGHT + Fore.MAGENTA + f'\tTimed out getting comparisons results' + Style.RESET_ALL)

atexit.register(Api.printReport)
