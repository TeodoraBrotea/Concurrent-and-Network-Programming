import urllib.request as req
from threading import Thread

class DownloadThread(Thread):
    def __init__(self, url, name):
        super().__init__()
        self.name = name
        self.url = url

    def run(self):
        self.download()

    def download(self):
        req.urlretrieve(self.url, self.name)

class DecryptThread(Thread):
    def __init__(self, file, offset):
        super().__init__()
        self.file = file
        self.offset = offset
        self.cipher = ""

    def cipher_decryption(self):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        cipher = ''
        with open(self.file) as file:
            lines = file.read()

            for letter in lines:
                if letter.lower() in alphabet:
                    cipher += alphabet[(alphabet.index(letter) - self.offset) % (len(alphabet))]
                else:
                    cipher += letter
            file.close()

        return cipher

    def run(self):
        self.cipher = self.cipher_decryption()


class Combiner:
    def __init__(self, message):
        self.message = message

    def write_message(self):
        with open("s_final.txt", 'w') as file:
            for msg in self.message:
                file.write(msg)
                file.write("\n\n")


if __name__ == "__main__":

    file_s1 = 's1.txt'
    file_s2 = 's2.txt'
    file_s3 = 's3.txt'

    download_thread_s1 = DownloadThread('https://advancedpython.000webhostapp.com/s1.txt', file_s1)
    download_thread_s2 = DownloadThread('https://advancedpython.000webhostapp.com/s2.txt', file_s2)
    download_thread_s3 = DownloadThread('https://advancedpython.000webhostapp.com/s3.txt', file_s3)

    download_thread_s1.start()
    download_thread_s2.start()
    download_thread_s3.start()

    download_thread_s1.join()
    download_thread_s2.join()
    download_thread_s3.join()

    decrypt_thread_s1 = DecryptThread(file_s1, 8)
    decrypt_thread_s2 = DecryptThread(file_s2, 8)
    decrypt_thread_s3 = DecryptThread(file_s3, 8)

    decrypt_thread_s1.start()
    decrypt_thread_s2.start()
    decrypt_thread_s3.start()

    decrypt_thread_s1.join()
    decrypt_thread_s2.join()
    decrypt_thread_s3.join()

    decrypted_text = [decrypt_thread_s1.cipher, decrypt_thread_s2.cipher, decrypt_thread_s3.cipher ]

    combiner = Combiner(decrypted_text)

    combiner.write_message()

    with open("s_final.txt", 'r') as file:
        print(file.read())
