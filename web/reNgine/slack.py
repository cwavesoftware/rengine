#!/usr/bin/python3

import os, sys, json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging

SLACK_USER = ""
client = WebClient(token=os.environ["SLACK_TOKEN"])


def getFiles(user=SLACK_USER):
    files = []
    page = 1
    while True:
        logging.info(f"Getting files of user {user}, page {page} ...")
        filesperPage = client.files_list(user=user, page=page).data["files"]
        files += filesperPage
        page += 1
        if len(filesperPage) == 0:
            break
    return files


def uploadFile(fpath, fname):
    with open(fpath, "rb") as fin:
        fcontent = fin.read()
        logging.info(
            f"Uploading {fpath} under name {fname}, size = {len(fcontent)} ..."
        )
        result = client.files_upload(file=fcontent, filename=fname)
        logging.debug(result)
        if result.data["ok"]:
            return result.data["file"]
        else:
            logging.error(f"Could not upload the file, error = {result.data['error']}")


def uploadFileIfNotExists(fpath, fname, existingFiles, user=SLACK_USER):
    exist, fileInfo = fileExists(
        fname,
        existingFiles,
        user,
    )
    if not exist:
        logging.info("File does not exists")
        result = uploadFile(fpath, fname)
        logging.info(f"File uploaded, ID = {result['id']}")
        return result
    else:
        logging.info(f'File exists, ID = {fileInfo["id"]}')
        return fileInfo


def fileExists(fname, existingFiles, user=SLACK_USER):
    logging.info(f"Checking if file {fname} exists ...")
    if existingFiles:
        files = existingFiles
    else:
        files = getFiles(user)
    for file in files:
        if file["name"] == fname:
            return True, file
    return False, None


def publishFile(fileId):
    logging.info(f"Publishing file {fileId}")
    try:
        result = client.files_sharedPublicURL(file=fileId).data
        logging.debug(result)
        fileInfo = result["file"]
    except SlackApiError as ex:
        if ex.response.data["error"] == "already_public":
            logging.warning(f"File {fileId} is already public. Getting its info ...")
            fileInfo = getFileInfo(fileId)
        else:
            logging.error(ex)
            return None
    except Exception as ex:
        logging.error(ex)
        return None

    return f"{fileInfo['url_private']}?pub_secret={fileInfo['permalink_public'].split('-')[-1]}"


def uploadAndPublish(fpath, fname, existingFiles, user=SLACK_USER):
    fileInfo = uploadFileIfNotExists(fpath, fname, existingFiles, user)
    if not fileInfo:
        return None
    if not fileInfo["is_public"]:
        url_public = publishFile(fileInfo["id"])
        if not url_public:
            return None
        logging.info(f"File published: {url_public}")
    else:
        url_public = f"{fileInfo['url_private']}?pub_secret={fileInfo['permalink_public'].split('-')[-1]}"
    return url_public


def upload(fpath, fname, existingFiles, user=SLACK_USER):
    try:
        fileInfo = uploadFileIfNotExists(fpath, fname, existingFiles, user)
        logging.info(fileInfo)
        return fileInfo["id"]
    except Exception as ex:
        logging.error(ex)
        return None


def getFileInfo(fileId):
    result = client.files_info(file=fileId)
    if result.data["ok"]:
        return result.data["file"]


if __name__ == "__main__":
    try:
        api_response = client.api_test()
        logging.info("Slack API status OK")
    except:
        logging.error("Cannot call Slack API")
