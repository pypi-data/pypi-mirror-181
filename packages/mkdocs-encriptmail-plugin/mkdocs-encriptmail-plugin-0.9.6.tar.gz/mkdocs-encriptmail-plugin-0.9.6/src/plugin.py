# plugin.py

import re
import os

from bs4 import BeautifulSoup
from mkdocs import utils
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

base_path = os.path.dirname(os.path.abspath(__file__))

class encriptMailPlugin(BasePlugin):
    config_scheme = (
        ("placeholderAt", config_options.Type(str, default="@")),
        ("placeholderDot", config_options.Type(str, default="."))
    )
    

    def on_post_page(self, output, page, config, **kwargs):
        """Add javascript javascript code """
        soup = BeautifulSoup(output, "html.parser")
        if soup.head:
            js_script = soup.new_tag("script")
            js_script.attrs["src"] = utils.get_relative_url(
                utils.normalize_url("assets/javascripts/encriptmail.js"), page.url
            )
            soup.head.append(js_script)
        return str(soup)

    def on_post_build(self, config, **kwargs):
        """Copy glightbox"s css and js files to assets directory"""

        output_base_path = os.path.join(config["site_dir"], "assets")
        
        js_path = os.path.join(output_base_path, "javascripts")
        utils.copy_file(
            os.path.join(base_path, "js", "encriptmail.js"),
            os.path.join(js_path, "encriptmail.js"),
        )


    def on_page_markdown(self, markdown, page, config, **kwargs):
        """Search after E-Mail addresses"""
        pattern = re.compile(r'\[(.*?)\]\((mailto:[a-zA-Z0-9_.+-]+@(?:(?:[a-zA-Z0-9-]+\.)?[a-zA-Z]+\.[a-zA-Z0-9]+))\)', flags=re.IGNORECASE)
        markdown = re.sub(pattern, self.__replace, markdown)     
        return markdown

    def __isMail(self, text):
        ret = False
        isMail = re.search(r'[a-zA-Z0-9_.+-]+@(?:(?:[a-zA-Z0-9-]+\.)?[a-zA-Z]+\.[a-zA-Z0-9]+)',text)
        if isMail != None:
            ret = True
        return ret

    def __decryptString(self, text, shift):
        result = ""
        # transverse the plain text
        for i in range(len(text)):
            char = text[i]
            n = ord(char)
            if (n >= 0x2B and n <= 0x3A):
                result += self.__decryptCharcode(n,0x2B,0x3A,shift)
            else:
                if (n >= 0x40 and n <= 0x5A):
                    result += self.__decryptCharcode(n,0x40,0x5A,shift)
                else:
                    if (n >= 0x61 and n <= 0x7A):
                       result += self.__decryptCharcode(n,0x61,0x7A,shift)
                    else:
                        result += char
        return result

    def __decryptCharcode(self, n, start, end, offset):
        n = n + offset;
        if (offset > 0) and (n > end):
            n = start + (n - end - 1)
        else: 
            if (offset < 0 and n < start):
                 n = end - (start - n - 1)
        return chr(n)

    def __replace(self, m):
        matchedString = m.group(0)
        linktext = m.group(1)
        mail = m.group(2)

        if self.__isMail(linktext):
            linktext=linktext.replace("@", self.config.get("placeholderAt", "(Q)"))
            linktext=linktext.replace(".", self.config.get("placeholderDot", "."))

        mail = self.__decryptString(mail ,+2)

        ret = '<a href="javascript:linkTo_UnCryptMailto(%27' +mail+ '%27)">'+linktext+'</a>'
        return ret