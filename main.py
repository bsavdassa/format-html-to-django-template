import os
import sys

TARGET_HTML:str = "index.html";
class AutomakeTemplateStatic:
    def __init__(self, file:str, targetFile:str) -> None:
        self.file:str = file;
        self.targetFile:str = targetFile;

    def readFile(self) -> str:
        with open(self.file, "r+", encoding="utf8") as f:
            return f.read();

    def writeFile(self, content:str):
        with open(self.targetFile, "w+", encoding="utf8") as f:
            f.write(content);
        return;

    def main(self):
        content = self.readFile();
        content = ("{% load static %}" if not content.startswith("{% load static %}") else "") + content;
        replaceStart:int = -1;
        replaceEnd:int = -1;
        for i in range(len(content)):
            tagLength = i+5 if any(x in content[i:i+5] for x in ["href =", "href="]) else i + 4 if any(x in content[i:i+4] for x in ["src =", "src="]) else -1;
            if (tagLength > -1):
                i2:int = tagLength;
                quoteStart:int = -1;
                quoteEnd:int = -1;
                while quoteStart < 0:
                    if (content[i2] == "\""):
                        quoteStart = i2;
                        replaceStart = i2;
                        continue;
                    if (content[i2] in [">", "/>"]):
                        raise SyntaxError(i2);
                    if (i2 == len(content) -1): raise ValueError(i2); 
                    i2+=1;
                i2+=1;
                while quoteEnd < 0:
                    if (content[i2] == "\""):
                        quoteEnd = i2
                        replaceEnd = i2;
                        continue;
                    if (content[i2] in ["<",]):
                        raise SyntaxError(i2);
                    if (i2 == len(content) -1): raise ValueError(i2); 
                    i2+=1;
                replaceStart += 1;
                if (replaceStart != replaceEnd and (not any(content[replaceStart:replaceEnd].startswith(x) for x in ["#", "https://", "http://", "{"])) and (not any(content[replaceStart:replaceEnd].endswith(x) for x in [".html", "#", ";", "}"])) ):
                    content = content[:replaceStart] + "{"+f"% static {content[replaceStart:replaceEnd]} %"+"}" + content[replaceEnd:];
        self.writeFile(content);
if __name__ == "__main__":
    if (len(sys.argv)>1):
        for file in os.listdir(sys.argv[1]):
            sys.argv[1] = sys.argv[1][:-1] if any(sys.argv[1][-1] == x for x in ["/", "\\"]) else sys.argv[1]; 
            absPath = sys.argv[1]+"/"+file;
            if (file.endswith(".html") and os.path.isfile(absPath)):
                AutomakeTemplateStatic(absPath, absPath).main();
    AutomakeTemplateStatic("index.html", "index-copy.html").main();