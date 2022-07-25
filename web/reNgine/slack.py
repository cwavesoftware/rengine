#!/usr/bin/python3

import os, sys, json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
if __name__ != '__main__':
    from .definitions import *
else:
    import logging
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

SLACK_USER = os.environ['SLACK_USER']

client = WebClient(token=os.environ['SLACK_TOKEN'])
try:
    api_response = client.api_test()
    logger.info('Slack API status OK')
except:
    logger.error('Cannot call Slack API')


def getFiles(user=SLACK_USER):
    files = []
    page = 1
    while True:
        logger.info(f'Getting files of user {user}, page {page} ...')
        filesperPage = client.files_list(user=user, page=page).data['files']
        files += filesperPage
        page += 1
        if len(filesperPage) == 0:
            break
    return files

def uploadFile(fpath, fname):
    with open(fpath, 'rb') as fin:
        fcontent = fin.read()
        logger.info(f"Uploading {fpath} under name {fname}, size = {len(fcontent)} ...")
        result = client.files_upload(file=fcontent,filename=fname)
        logger.debug(result)
        if result.data['ok']:
            return result.data['file']
        else:
            logger.error(f"Could not upload the file, error = {result.data['error']}")

def uploadFileIfNotExists(fpath, fname, existingFiles, user=SLACK_USER):
    exist, fileInfo =  fileExists(fname, existingFiles, user, )
    if not exist:
        logger.info('File does not exists')
        result = uploadFile(fpath, fname)
        logger.info(f"File uploaded, ID = {result['id']}")
        return result
    else:
        logger.info(f'File exists, ID = {fileInfo["id"]}')
        return fileInfo

def fileExists(fname, existingFiles, user=SLACK_USER):
    logger.info('Checking if file exists ...')
    if existingFiles:
        files = existingFiles
    else:
        files = getFiles(user)
    for file in files:
        if file['name'] == fname:
            return True, file
    return False, None


def publishFile(fileId):
    logger.info(f'Publishing file {fileId}')
    try:
        result = client.files_sharedPublicURL(file=fileId).data
        logger.debug(result)
        fileInfo = result['file']
    except SlackApiError as ex:
        if ex.response.data['error'] == 'already_public':
            logger.warning(f'File {fileId} is already public. Getting its info ...')
            fileInfo = getFileInfo(fileId)

    return f"{fileInfo['url_private']}?pub_secret={fileInfo['permalink_public'].split('-')[-1]}"



def uploadAndPublish(fpath, fname, existingFiles, user=SLACK_USER):
    fileInfo = uploadFileIfNotExists(fpath, fname, existingFiles, user)
    if not fileInfo:
        return
    if not fileInfo['is_public']:
        url_public = publishFile(fileInfo['id'])
        logger.info(f"File published: {url_public}")
    else:
        url_public = f"{fileInfo['url_private']}?pub_secret={fileInfo['permalink_public'].split('-')[-1]}"
    return url_public


def getFileInfo(fileId):
    result = client.files_info(file=fileId)
    if result.data['ok']:
        return result.data['file']


if __name__ == '__main__':
    uploadAndPublish('/Users/cosmincraciun/superbet/logo.png', 'logo9', SLACK_USER)