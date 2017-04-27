import os,sys
from hashlib import md5
reload(sys)
sys.setdefaultencoding('utf-8')

def md5_file(name):
    m = md5()
    a_file = open(name, 'rb')
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()

PWD = '/Users/zen/Workspace/src/search_planner/sp_coder/workspace/'



class FileTool:

    def listAllFile(self, path, res):
        if not os.path.isdir(path):
            return

        files = os.listdir(path)
        for f in files:
            if f[0] == '.':
                continue

            p = path + "/" + f
            if os.path.isdir(p):
                self.listAllFile(p, res)
            else:
                res.append(p)


    def listDir(self, path):
        res = {}
        if not os.path.isdir(path):
            return res

        files = os.listdir(path)
        for f in files:
            if f[0] == '.':
                continue
            p = path + "/" + f
            if os.path.isdir(p):
                res[f] = self.listDir(p)
            else:
                res[f] = md5_file(p)

        return res

    def writeFile(self, path, content):
        if os.path.isdir(path):
            return False

        f = open(path, 'w+')
        f.write(content)
        f.close()
        return True

    def makeDir(self, path):
        if os.path.isdir(path):
            return False
        print(path)
        os.mkdir(path)
        return True

    def readFile(self, path):
        if not os.path.exists(path):
            return False

        if os.path.isdir(path):
            return self.listDir(path)

        f = open(path, 'r')
        res = f.read()
        f.close()
        return res

    def delFile(self,path):
        if not os.path.exists(path):
            return False

        if os.path.isdir(path):
            os.rmdir(path)
            return True

        os.remove(path)
        return True
