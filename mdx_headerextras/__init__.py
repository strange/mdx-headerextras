import markdown
import re

HEADER_LEVEL_RE = re.compile('h([1-6])')
ALPHANUM_RE = re.compile('\W+')

def makeExtension(configs=None):
    return HeaderExtrasExtension(configs=configs or {})
    
class HeaderExtrasExtension(markdown.Extension):
    def __init__(self, configs):
        self.proc_config = {}
        for k, v in configs:
            if k in ('prefix', 'level'):
                self.proc_config[str(k)] = v
        markdown.Extension.__init__(self, configs)

    def extendMarkdown(self, md, md_globals):
        processor = HeaderExtrasProcessor(**self.proc_config)
        md.treeprocessors.add('headerextras', processor, '_end')


class HeaderExtrasProcessor(markdown.treeprocessors.Treeprocessor):
    def __init__(self, level=1, prefix='section-'):
        self.level = level
        self.prefix = prefix
        markdown.treeprocessors.Treeprocessor.__init__(self)

    def run(self, node):
        for child in node.getiterator():
            match = HEADER_LEVEL_RE.match(child.tag)
            if match:
                child.set('id', self._make_id(child.text))
                if self.level != 1:
                    level = int(match.groups()[0]) + int(self.level) - 1
                    child.tag = 'h%s' % level
        return node

    def _make_id(self, s):
        s = s.replace(' ', '_')
        s = ALPHANUM_RE.sub('', s)
        s = s.replace('_', '-')
        s = s.lower()
        s = s.strip()
        return '%s%s' % (self.prefix, s)
