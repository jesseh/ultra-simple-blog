import os
import re

from django.core.management.base import NoArgsCommand
from django.core.management.commands import cleanup


class Command(NoArgsCommand):
    help = "Generate a list of expected behavior based on the test suite."
    
    def _test_lines(self):
        """
        A generator of all the lines in all the test files.
        """
        filenames = os.popen('find apps -name "*test*.py"')
        for filename in filenames:
            filename = filename.strip()
            print("Searching %s..." % filename)
            for line in open(filename, "r"):
                yield(line)

    def _un_camel_case(self, str):
        """
        Change camel case into looking like a sentence.
        """
        return(re.sub(r"(.)(?=[A-Z])", r"\1 ", str))

    def handle_noargs(self, *args, **kwargs):
        patterns = { "class": r"\s*class ([^(]*)\(",
                     "test": r"\s*def test([^(]*)\(",
                   }
        expectations = ""
        for line in self._test_lines():
            if line:
                for role, pattern in patterns.items():
                    res = re.match(pattern, line)
                    if res:
                        if role == "class": 
                            expectations += "%s:\n" % (self._un_camel_case(res.group(1)).capitalize())
                        elif role == "test": 
                            how = res.group(1)
                            if not how: how = "o"
                            expectations += "  - %s.\n" % (self._un_camel_case(res.group(1)).lower())
                        break
        if not expectations: expectations = "(none)"
        print "\n\n---\n%s\n---\n" % expectations

        cleanup.Command().execute()
        print("done")
