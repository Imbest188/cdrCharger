import subprocess


class AsnDecoder:
    @staticmethod
    def decode(file, programPath='asn/casndecoder.exe', workPath='CDR/'):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen([programPath, workPath + file], startupinfo=si)
        p.communicate()
        return not p.returncode
