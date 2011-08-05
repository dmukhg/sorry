import unittest

class ObjectsTest(unittest.TestCase):
    def testBlocks(self):
        from filters import MarkdownFilter, PygmentsFilter
        from objects import Block
    

        # Testing Markdown Filter
        test_text = """
this is a heading
===

this is [link][1] to google

[1]: http://google.com/
"""
        test_output = u"<h1>this is a heading</h1>\n<p>this is \
<a href=\"http://google.com/\">link</a> to google</p>"

        b = Block(test_text, [MarkdownFilter()])
        self.assertEqual(b.render(), test_output)

        # Testing PygmentsFilter
        test_text = """
from future import *

class No:
    def nono:
        pass
"""

        test_output = u'<div class="highlight"><pre><span class="kn">from</span> <span class="nn">future</span> <span class="kn">import</span> <span class="o">*</span>\n\n<span class="k">class</span> <span class="nc">No</span><span class="p">:</span>\n    <span class="k">def</span> <span class="nf">nono</span><span class="p">:</span>\n        <span class="k">pass</span>\n</pre></div>\n'
        b = Block(test_text, [PygmentsFilter('python')])
        self.assertEqual(b.render(), test_output)
