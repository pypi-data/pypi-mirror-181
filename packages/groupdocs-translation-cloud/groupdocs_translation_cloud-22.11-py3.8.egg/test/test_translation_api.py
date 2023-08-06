# coding: utf-8

# """
# --------------------------------------------------------------------------------------------------------------------
#  <copyright company="Aspose" file="test_translation_api.py">
#    Copyright (c) 2020 GroupDocs.Translation for Cloud
#  </copyright>
#  <summary>
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
# 
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
# 
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# </summary>
# --------------------------------------------------------------------------------------------------------------------
# """

from __future__ import absolute_import

import os
import unittest
import sys
import shutil

from groupdocstranslationcloud.api.storage_api import StorageApi

sys.path.append('../')
import groupdocstranslationcloud.models
from groupdocstranslationcloud.models import translate_text, translate_document, translate_hugo
from groupdocstranslationcloud.rest import ApiException
from test_helper import TestHelper


class TestTranslationApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api = TestHelper.translation
        cls.storageApi = TestHelper.storage

    ###############################################################
    #                          Translation tests
    ###############################################################

    # def test_text_translation(self):
    #     pair = "en-fr"
    #     text = "Welcome to Paris"
    #     try:
    #         translator = translate_text.TranslateText(pair, text)
    #         request = translator.to_string()
    #         response = self.api.post_translate_text(request)
    #         self.assertEqual(response.status, "ok")
    #     except ApiException as ex:
    #         print("Exception")
    #         print("Info: " + str(ex))
    #         raise ex

    # def test_document_translation(self):
    #     pair = "en-fr"
    #     _format = "docx"
    #     outformat = "docx"
    #     storage = "First Storage"
    #     name = "test_file.docx"
    #     folder = "TranslationTestDoc"
    #     savepath = "TranslationTestDoc"
    #     savefile = "translated_test_python.docx"
    #     masters = False
    #     elements = None
    #
    #     src = TestHelper.get_local_folder() + "/" + name
    #     dst = TestHelper.get_folder() + "/" + name
    #     dst_trs = TestHelper.get_folder() + "/" + savefile
    #     src_trs = TestHelper.get_local_folder() + "/" + savefile
    #
    #     if self.storageApi.object_exists(dst).to_dict()['exists']:
    #         print(name, 'already exists')
    #     else:
    #         result = self.storageApi.upload_file(dst, src).to_dict()
    #         if len(result['errors']) == 0:
    #             print(result['uploaded'], "was uploaded")
    #         else:
    #             print(name, 'wasn\'t uploaded')
    #     try:
    #         translator = translate_document.TranslateDocument(pair, _format, outformat, storage, name, folder, savepath, savefile, masters, elements)
    #         request = translator.to_string()
    #         response = self.api.post_translate_document(request)
    #         self.assertEqual(response.status, "ok")
    #     except ApiException as ex:
    #         print("Exception")
    #         print("Info: " + str(ex))
    #         raise ex
    #
    #     result = self.storageApi.download_file(dst_trs)
    #     if result:
    #         print(savefile, "was downloaded")
    #     else:
    #         print(savefile, 'wasn\'t downloaded')
    #
    #     shutil.move(result, src_trs)
    #
    #     self.storageApi.delete_file(dst)
    #     self.storageApi.delete_file(dst_trs)

    def test_hugo_translation(self):
        storage = "First Storage"
        name = "hugo_test.md"
        folder = "TranslationTestDoc"
        shortcodedict = {0: [["title"], ["frontmatter", "title"], ["frontmatter", "description"]]}

        src = TestHelper.get_local_folder() + "/" + name
        dst = TestHelper.get_folder() + "/" + name

        # result = self.storageApi.upload_file(dst, src).to_dict()
        # if len(result['errors']) == 0:
        #     print(result['uploaded'], "was uploaded")
        # else:
        #     print(name, 'wasn\'t uploaded')

        try:
            translator = translate_hugo.TranslateHugo(name, folder, storage, shortcodedict)
            request = translator.to_string()
            print(request)
            response = self.api.post_translate_hugo(request)
            self.assertEqual(response.status, "ok")
        except ApiException as ex:
            print("Exception")
            print("Info: " + str(ex))
            raise ex
        print(response)
        # self.storageApi.delete_file(dst)

if __name__ == '__main__':
    unittest.main()
