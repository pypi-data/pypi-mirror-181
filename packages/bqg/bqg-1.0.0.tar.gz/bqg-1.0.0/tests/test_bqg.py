import bqg
import unittest
import xml.etree.ElementTree as et
from typing import Dict

class TestCommentQuestion(unittest.TestCase):

    def setUp(self) -> None:
        self.cq = bqg.CommentQuestion("ID1","Test Question?")
        self.xml = self.cq.get_xml()

    def test_comment_returns_xml(self):

        self.assertIsInstance(self.xml, et.Element)

    def test_comment_xml_has_right_static_values(self):

        # Check all tags exist.
        self.assertEqual(self.xml.tag, "commentQuestion")

        # Check static children of commentQuestion.
        children: Dict[str, str] = {"isPersonalize":"false","QuestionDisplayType":"All"}
        for child, value in children.items():
            child_xml = self.xml.find(child)
            self.assertIsNotNone(child_xml, f"Child {child} was not found.")

            self.assertEqual(child_xml.text, value, f"Value {value} for child {child} does not exist")
        
    def test_comment_internal_id_is_uuid_format(self):
        # Check that UUID exists.
        id_xml = self.xml.find("ID")
        self.assertIsNotNone(id_xml)

        # Check that the UUID matches the regex form.
        uuid = id_xml.text
        self.assertRegex(uuid, r"^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$")
        
    def test_identify_id_forms_properly(self):
        identify_id = self.xml.find("IdentifyID").text

        self.assertEqual(identify_id,"ID1")

    def test_question_title_forms_properly(self):
        question_title = self.xml.find("questionTitle")

        self.assertIsNotNone(question_title)
        question_text = question_title.find("caption").text
        question_id = question_title.find("caption").find("id").text

        self.assertEqual(question_text,"Test Question?")

        self.assertRegex(question_id, r"^questionnaire/commentBox/[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}/questionTitle@id=en-US$")

class TestRatingQuestion(unittest.TestCase):

    def setUp(self) -> None:
        options: Dict[str, str] = {"1": "Yes", "2": "No"}
        self.cq = bqg.RatingQuestion("ID1","Test Question?", options, "")
        self.xml = self.cq.get_xml()

    def test_returns_xml(self):

        self.assertIsInstance(self.xml, et.Element)

    def test_xml_has_right_static_values(self):

        # Check all tags exist.
        self.assertEqual(self.xml.tag, "ratingQuestion")

        # Check static children of commentQuestion.
        children: Dict[str, str] = {"isPersonalize":"false","QuestionDisplayType":"All"}
        for child, value in children.items():
            child_xml = self.xml.find(child)
            self.assertIsNotNone(child_xml, f"Child {child} was not found.")

            self.assertEqual(child_xml.text, value, f"Value {value} for child {child} does not exist")
        
    def test_internal_id_is_uuid_format(self):
        # Check that UUID exists.
        id_xml = self.xml.find("ID")
        self.assertIsNotNone(id_xml)

        # Check that the UUID matches the regex form.
        uuid = id_xml.text
        self.assertRegex(uuid, r"^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$")
        
    def test_identify_id_forms_properly(self):
        identify_id = self.xml.find("IdentifyID").text

        self.assertEqual(identify_id,"ID1")

    def test_question_title_forms_properly(self):
        question_title = self.xml.find("questionTitle")

        self.assertIsNotNone(question_title)
        question_text = question_title.find("caption").text
        question_id = question_title.find("caption").find("id").text

        self.assertEqual(question_text,"Test Question?")

        self.assertRegex(question_id, r"^questionnaire/ratingQuestion/[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}/questionTitle@id=en-US$")

    def test_rating_static_values_form_properly(self):
        child_xml = self.xml.find("isSingleRow")

        self.assertIsNotNone(child_xml)
        self.assertEqual(child_xml.text, "true")

    def test_primary_scale_forms_properly(self):
        primary_scale = self.xml.find("primaryScale")
        self.assertIsNotNone(primary_scale)

        display_as_radio_button = primary_scale.find("displayAsRadioButton").text
        self.assertEqual(display_as_radio_button,"true")

        scales = primary_scale.findall("scale")
        scale_scores = [x.find("score").text for x in scales]
        self.assertEqual(scale_scores, ["1","2",""])

class TestSectionBox(unittest.TestCase):

    def setUp(self) -> None:
        self.sb = bqg.SectionBox("Test Question?")
        self.xml = self.sb.get_xml()

    def test_returns_xml(self):
        self.assertIsInstance(self.xml, et.Element)

    def test_internal_id_is_uuid_format(self):
        # Check that UUID exists.
        id_xml = self.xml.find("ID")
        self.assertIsNotNone(id_xml)

        # Check that the UUID matches the regex form.
        uuid = id_xml.text
        self.assertRegex(uuid, r"^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$")
        
if __name__ == "__main__":
    unittest.main()