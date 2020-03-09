from PIL import Image
import os


class Redimensionar(object):

    def __init__(self, diretorio_imagem):
        self.diretorio_imagem = diretorio_imagem
        self.image = Image.open(diretorio_imagem).convert("RGB")

    def redimensionar(self, destino: str, dpi=(240, 240), largura_padrao=2000) -> bool:
        altura, largura = self.get_dimensoes()
        if largura < largura_padrao:
            return False

        percentual = largura_padrao / largura
        img = self.image.resize((int(altura * percentual), largura_padrao), Image.LANCZOS)
        extensao = os.path.splitext(destino)[1]
        img.save(destino.replace(extensao, '.jpg'), dpi=dpi)
        return True

    def get_tamanho_foto(self):
        return os.stat(self.diretorio_imagem).st_size

    def get_dimensoes(self):
        return self.image.size
