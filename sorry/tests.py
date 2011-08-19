import unittest
from objects import *

class ObjectsTest(unittest.TestCase):
    def testBlocksMarkdown(self):
        from filters import MarkdownFilter
        from objects import Block
        
        # Testing Markdown Filter
        test_text = " this is a heading\n===\n this is [link][1] to google\n [1]: http://google.com/ "
        test_output = u"<h1>this is a heading</h1>\n<p>this is <a href=\"http://google.com/\">link</a> to google</p>"

        b = Block(test_text, [MarkdownFilter()])
        self.assertEqual(b.render(), test_output)

    def testBlockPygments(self):
        from filters import PygmentsFilter
        from objects import Block

        # Testing PygmentsFilter
        test_text = "from future import *\n\nclass No:\n    def nono:\n        pass"

        test_output = u'<div class="highlight"><pre><span class="kn">from</span> <span class="nn">future</span> <span class="kn">import</span> <span class="o">*</span>\n\n<span class="k">class</span> <span class="nc">No</span><span class="p">:</span>\n    <span class="k">def</span> <span class="nf">nono</span><span class="p">:</span>\n        <span class="k">pass</span>\n</pre></div>\n'
        b = Block(test_text, [PygmentsFilter('python')])
        self.assertEqual(b.render(), test_output)

    def testPostDecompose(self):
        test_text = "this should be block 1\n::code:java\nimport java.io.*\n::endcode\nthis should be block 2\n::code:javascript\nx = x + 1;\n::endcode\n::code:python\nfrom __future__ import with_statement\n::endcode"

        test_output = []
        test_output.append(u'<p>this should be block 1</p>')
        test_output.append(u'<div class="highlight"><pre><span class="kn">import</span> <span class="nn">java.io.*</span>\n</pre></div>\n')
        test_output.append(u'<p>this should be block 2</p>')
        test_output.append(u'<div class="highlight"><pre><span class="nx">x</span> <span class="o">=</span> <span class="nx">x</span> <span class="o">+</span> <span class="mi">1</span><span class="p">;</span>\n</pre></div>\n')
        test_output.append(u'<div class="highlight"><pre><span class="kn">from</span> <span class="nn">__future__</span> <span class="kn">import</span> <span class="n">with_statement</span>\n</pre></div>\n')

        p = Post(test_text, {'uid':1, 'date': "July, 2010", 'author': 'dmu', 'title': "Title 1"})
        blocks = p.decompose()

        print len(blocks)
        for block in blocks:
            self.assertEqual(block.render(), test_output[blocks.index(block)])


class ProcessTest(unittest.TestCase):
    def setUp(self):
        import os 
        cwd = os.path.split(__file__)[0]
        self.test_dir = os.path.join(cwd, 't')
        self.test_layout_dir = os.path.join(self.test_dir, 'layout')
        self.test_layout_template = os.path.join(self.test_layout_dir, 'base.html')
        self.test_post_dir = os.path.join(self.test_dir, 'posts')
        self.test_post_file = os.path.join(self.test_post_dir, '1.md')
        self.test_post_file2 = os.path.join(self.test_post_dir, '2.md')

    def testList_of_files(self):
        from processes import list_of_files
        import os
        
        l = list_of_files(self.test_post_dir)
        self.assertEqual(len(l),len(os.listdir(self.test_post_dir)))
        # this test needs improvement. It merely checks that the
        # number of objects returned is equal to the number of files
        # in the directory.

        for _ in l:
            assert(isinstance(_, file))

    def testPost_from_file(self):
        from processes import post_from_file

        p = post_from_file(open(self.test_post_file))
        
        assert(isinstance(p, Post))
        self.assertEqual(p.uid, '1')

    def testRender_html(self):
        from processes import render_html, post_from_file
        from objects import Link
        from mako.template import Template

        p1 = post_from_file(open(self.test_post_file))     
        p2 = post_from_file(open(self.test_post_file2))
          
        posts = [p1, p2]
        footlinks = [Link("http://github.com/", "github"), Link("http://github.com/schatten/", "my github")]
        template = Template(open(self.test_layout_template).read())
        title = "Hello World"

        self.assertEqual(render_html(posts, title, footlinks, template),
                u'<html>\n    <head>\n        <title>Hello World | sitename.com</title>\n    </head>\n    <body>\n        <h1>Hello World</h1>\n\n            July, 2007\n            <a href="/archive/1.html">Post 1</a>\n            <p>contents</p>\n            July, 2007\n            <a href="/archive/2.html">Post 2</a>\n            <p>contents</p>\n\n        <a href="http://github.com/">github</a>\n        <a href="http://github.com/schatten/">my github</a>\n    </body>\n</html>\n'
                )

    def testIndices(self):
        from processes import create_indices
        from mako.template import Template

        template = Template(open(self.test_layout_template).read())
        sitename = "sitename"

        index_map = create_indices(self.test_post_dir, sitename, template)

        self.assertEqual(len(index_map), 3)
        # this assumes that the post_per_index value is 3
        self.assertEqual(index_map['page-2'],  
                 u'<html>\n    <head>\n        <title>sitename | sitename.com</title>\n    </head>\n    <body>\n        <h1>sitename</h1>\n\n            July, 2007\n            <a href="/archive/4.html">Post 4</a>\n            <p>contents</p>\n            July, 2007\n            <a href="/archive/5.html">Post 5</a>\n            <p>contents</p>\n            July, 2007\n            <a href="/archive/6.html">Post 6</a>\n            <p>contents</p>\n\n        <a href="index">newer</a>\n        <a href="page-3">older</a>\n    </body>\n</html>\n'
                 )


class DispatchTest(unittest.TestCase):
    def setUp(self):
        import os, subprocess
        cwd = os.path.split(__file__)[0]
        self.test_dir = os.path.join(cwd, 't')
        
        # clean the deploy directory
        try:
            subprocess.call('rm -rf %s/deploy' %self.test_dir)
        except OSError:
            print "File doesn't exist : %s/deploy" %self.test_dir

    def testSitegen(self):
        from dispatch import sitegen

        sitegen(self.test_dir)
