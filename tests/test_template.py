import unittest
from types import StringType
from jinja2 import Template as _Template
from core.template import (Template,
                           NotSuchTemplateFileException, )


class TemplateTests(unittest.TestCase):
    filename = 'hello/index.html'
    faulty_filename = 'some/other/path'

    def test_it_should_load_the_file(self):
        output = Template().get_template_file(self.filename)
        self.assertIsInstance(output, StringType)
        self.assertTrue(len(output) > 0)

    def test_it_should_raise_an_exception_if_file_does_not_exists(self):
        with self.assertRaises(NotSuchTemplateFileException) as e:
            Template(self.faulty_filename).render()
        self.assertEqual(e.exception.code, '0')

    def test_it_should_autoload_file(self):
        template = Template(self.filename)
        self.assertIsInstance(template.template, _Template)


if __name__ == '__main__':
    unittest.main()
