import re,json,requests,shutil,urllib3
from random import randrange
from requests.structures import CaseInsensitiveDict
from tqdm.auto import tqdm
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_download_info(url,app_name):
	headers = CaseInsensitiveDict()
	headers["Device-Id"] = "ddd7d0612e8399d8474db2162f00286bbca52a13"
	headers["Accept-Language"] = "fa"
	headers["Is-Kid"] = "false"
	headers["User-Agent"] = "Bazaar/1300700 (Android 22; samsung SM-G973N)"
	headers["Client-Id"] = "9I3wVtDMTWSstWU0uwHsog"
	headers["Ad-Id"] = "3d6bf5ea-9690-4933-b14c-502cccabf711"
	headers["Android-Id"] = "b57b4fc67716e090"
	headers["Content-Type"] = "application/json; charset=UTF-8"
	headers["Content-Length"] = "1338"
	headers["Host"] = "api.cafebazaar.ir"
	headers["Connection"] = "Keep-Alive"
	headers["Accept-Encoding"] = "gzip"
	payload={"properties":{"androidClientInfo":{"adId":"3d6bf5ea-9690-4933-b14c-502cccabf711","adOptOut":False,"androidId":"b57b4fc67716e090","city":"NA","country":"NA","cpu":"x86,armeabi-v7a,armeabi","device":"","deviceType":0,"dpi":240,"hardware":"","height":1280,"locale":"fa","manufacturer":"samsung","mcc":432,"mnc":11,"mobileServiceType":1,"model":"SM-G973N","osBuild":"","product":"beyond1qlteue","province":"NA","sdkVersion":22,"width":720},"appThemeState":0,"clientID":"9I3wVtDMTWSstWU0uwHsog","clientVersion":"13.7.0","clientVersionCode":1300700,"isKidsEnabled":False,"language":2},"singleRequest":{"appDownloadInfoRequest":{"packageName":app_name,"downloadStatus":1,"referrers":[{"type":11,"extraJson":"{\"service\":\"vitrin\",\"slug\":\"home-game-contenttest\",\"groups\":\"cct:em\"}"},{"type":19,"extraJson":"{\"service\":\"vitrin\"}"},{"type":21,"extraJson":"{\"service\":\"vitrin\",\"slug\":\"home-game\"}"},{"type":1,"extraJson":"{\"service\":\"vitrin\",\"index\":4,\"title\":\"بازی‌های دیتادار\",\"source\":\"normal\",\"is_shuffled\":true,\"referrer_identifier\":\"query_Data Games\"}"},{"type":2,"extraJson":"{\"service\":\"vitrin\",\"index\":0,\"referrer_identifier\":\"\"}"}]}}}
	response=requests.post(url,json=payload,verify=False)
	data=response.json()
	return data

def appName(app_name, link):
	url = 'https://api.cafebazaar.ir/rest-v1/process/AppDetailsV2Request'
	payload = {
		"properties": {"androidClientInfo":{"adId":"3d6bf5ea-9690-4933-b14c-502cccabf711","adOptOut":False,"androidId":"b57b4fc67716e090","city":"NA","country":"NA","cpu":"x86,armeabi-v7a,armeabi","device":"","deviceType":0,"dpi":240,"hardware":"","height":1280,"locale":"fa","manufacturer":"samsung","mcc":432,"mnc":11,"mobileServiceType":1,"model":"SM-G973N","osBuild":"","product":"beyond1qlteue","province":"NA","sdkVersion":22,"width":720},"appThemeState":0,"clientID":"9I3wVtDMTWSstWU0uwHsog","clientVersion":"13.7.0","clientVersionCode":1300700,"isKidsEnabled":False,"language":2},"singleRequest":{"appDownloadInfoRequest":{"packageName":app_name,"downloadStatus":1,"referrers":[{"type":11,"extraJson":"{\"service\":\"vitrin\",\"slug\":\"home-game-contenttest\",\"groups\":\"cct:em\"}"},{"type":19,"extraJson":"{\"service\":\"vitrin\"}"},{"type":21,"extraJson":"{\"service\":\"vitrin\",\"slug\":\"home-game\"}"},{"type":1,"extraJson":"{\"service\":\"vitrin\",\"index\":4,\"title\":\"بازی‌های دیتادار\",\"source\":\"normal\",\"is_shuffled\":true,\"referrer_identifier\":\"query_Data Games\"}"},{"type":2,"extraJson":"{\"service\":\"vitrin\",\"index\":0,\"referrer_identifier\":\"\"}"}]}},
		"singleRequest": {
			"appDetailsV2Request": {
				"packageName": app_name,
			}
		}
	}

	response = requests.post(url, json=payload)
	if response.status_code== 200:
		data = json.loads(response.text)
		apkName = data['singleReply']['appDetailsV2Reply']['meta']['name']
		return apkName

	else:
		print("connection error with  ",response.status_code)
		exit()

def Dowload(link,path="./"):
	url = "https://api.cafebazaar.ir/rest-v1/process/AppDownloadInfoRequest"
	if "?" in link:
		regex = r"https://cafebazaar\.ir/app/(.*)(?:\?|\\)"
		matches = re.match(regex, link)
		app_name = matches.group(1).replace("/","")
	else:
		regex = r"https://cafebazaar\.ir/app/(.*)"
		matches = re.match(regex, link)
		print(matches.groups())
		app_name = (matches.group(1)).replace("/","")
	data = get_download_info(url,app_name)
	size = int(data['singleReply']['appDownloadInfoReply']['packageSize']) / 1000000
	name = appName(app_name,link)
	print("name : ",name,"size: ",size,"MB")
	urlDownload = "https://appcdn.cafebazaar.ir/apks/" + data['singleReply']['appDownloadInfoReply']['token']

	with requests.get(urlDownload,verify=False,stream=True) as response:
		if response.status_code ==200:
			total_length = int(response.headers.get("Content-Length"))
			name =  path+app_name + str(randrange(1000, 9999)) + '.apk'
			with tqdm.wrapattr(response.raw, "read", total=total_length, desc="") as raw:
				with open(name, 'wb') as output:
					shutil.copyfileobj(raw, output)
		else:
			print("error with status code ",response.status_code)



if __name__ == "__main__":
	Dowload("https://cafebazaar.ir/app/com.turbo.moin?l=en")


