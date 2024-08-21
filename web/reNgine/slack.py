#!/usr/bin/python3

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
import json
from celery.utils.log import get_task_logger
from scanEngine.models import Notification

logger = get_task_logger(__name__)

SLACK_USER = ""
SLACK_TOKEN = ""
try:
    notif = Notification.objects.all()
    if notif and notif[0]:
        SLACK_TOKEN = notif[0].slack_token
        client = WebClient(token=SLACK_TOKEN)
        logger.info("slack client instantiated successfully")
    else:
        raise Exception("could not get slack settings")
except Exception as ex:
    logger.error(ex)


def getFiles(user=SLACK_USER):
    files = []
    page = 1
    while True:
        logger.info(f"Getting files of user {user}, page {page} ...")
        retries = 0
        while retries < 3:
            try:
                filesperPage = client.files_list(user=user, page=page).data["files"]
                retries = 3
            except Exception as ex:
                logger.error(ex)
                retries += 1
        files += filesperPage
        page += 1
        if len(filesperPage) == 0:
            break
    return files


def uploadFile(fpath, fname):
    with open(fpath, "rb") as fin:
        fcontent = fin.read()
        logger.info(f"Uploading {fpath} under name {fname}, size = {len(fcontent)} ...")
        retries = 0
        while retries < 3:
            try:
                result = client.files_upload(file=fcontent, filename=fname)
                retries = 3
            except Exception as ex:
                logger.error(ex)
                retries += 1
        logger.debug(result)
        if result.data["ok"]:
            return result.data["file"]
        else:
            logger.error(f"Could not upload the file, error = {result.data['error']}")


def uploadFileIfNotExists(fpath, fname, existingFiles, user=SLACK_USER):
    exist, fileInfo = fileExists(
        fname,
        existingFiles,
        user,
    )
    if not exist:
        logger.info("File does not exists")
        result = uploadFile(fpath, fname)
        logger.info(f"File uploaded, ID = {result['id']}")
        return result
    else:
        logger.info(f'File exists, ID = {fileInfo["id"]}')
        return fileInfo


def fileExists(fname, existingFiles, user=SLACK_USER):
    return False, None  # little hack
    logger.info(f"Checking if file {fname} exists ...")
    if existingFiles:
        files = existingFiles
    else:
        files = getFiles(user)
    for file in files:
        if file["name"] == fname:
            return True, file
    return False, None


def publishFile(fileId):
    logger.info(f"Publishing file {fileId}")
    try:
        result = client.files_sharedPublicURL(file=fileId).data
        logger.debug(result)
        fileInfo = result["file"]
    except SlackApiError as ex:
        if ex.response.data["error"] == "already_public":
            logger.warning(f"File {fileId} is already public. Getting its info ...")
            fileInfo = getFileInfo(fileId)
        else:
            logger.error(ex)
            return None
    except Exception as ex:
        logger.error(ex)
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
        logger.info(f"File published: {url_public}")
    else:
        url_public = f"{fileInfo['url_private']}?pub_secret={fileInfo['permalink_public'].split('-')[-1]}"
    return url_public


def upload(fpath, fname, existingFiles, user=SLACK_USER):
    try:
        fileInfo = uploadFileIfNotExists(fpath, fname, existingFiles, user)
        logger.info(fileInfo)
        return fileInfo["id"]
    except Exception as ex:
        logger.error(ex)
        return None


def getFileInfo(fileId):
    result = client.files_info(file=fileId)
    if result.data["ok"]:
        return result.data["file"]
