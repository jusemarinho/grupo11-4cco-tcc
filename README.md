<h1>Aplicação de IA e RP para análises e identificação de animais domésticos abandonados</h1>

<p>Este é um projeto voltado a causa de cachorros e gatos abandonados, que por meio de reconhecimento de imagens e algoritmos de ML, 
conseguiremos escanear o rosto, características e o fucinho de um pet perdido na rua, e se o dono tiver cadastrado o pet em nosso sistema, 
por meio do reconehcimentovamos informar informações sobre o cachorro e como contatar o dono, para poder ser feito o resgate do animal.</p>

<h3>Tecnologias utilizadas</h3>
<ul>
  <li>Python 3.11</li>
  <li>Jupyter notebook</li>
  <li>Pandas</li>
  <li>Numpy</li>
  <li>Haarcascade Frontal Cat Face</li>
  <li>Scikit Learn</li>
  <li>Behave</li>
  <li>Boto3</li>
  <li>Fordev</li>
  <li>Pillow</li>
  <li>tqdm</li>
  <li>Dotenv</li>
  <li>aiohttp</li>
</ul>

<h3>Como rodar o projeto</h3>
<p>Ao fazer o clone do nosso projeto, instale as dependências python, contidas no arquivo requirements.txt usando o comando 
<code>pip install -r requirements.txt</code>.</p>
<p>Após instalar as dependências, crie um arquivo chamado <code>.env</code> na pasta raiz do projeto e coloque suas credencias da AWS. Vide exemplo: </p>
<code>AWS_ACCESS_KEY_ID= <br>
 AWS_SECRET_ACCESS_KEY= <br>
 AWS_ACCESS_TOKEN= <br> 
 AWS_DEFAULT_REGION=
</code>
<br>
<p>Temops 3 scripts python para serem executados, que são: </p>
<ul>
  <li>
    <b>dados_usuarios.ipynb:</b> Este script irá criar o nosso dataset com as informações do usuário. 
  </li>
  <li>
    <b>limpeza.ipynb:</b> Este script faz o tratamento dos dados, separando as dimensões que iremos utilizar; 
    a união dos datasets de gato e cachorro em um dataset só; obtém as fotos dos cachorros e fazer a conversão para base64; 
  </li>
  <li>
    <b>tratar_imagens.ipynb:</b> Aqui iremos fazer a relação do dataset dos pets com os usuários, para que cada usuário que criamos, tenha, por regra,
    até 9 pets e no mínimo 1 pet. Após a relação, iremos salvar as imagens dos cachorro no S3, usando o conceito de diretórios do storage, cada usuário terá
    um diretório e dentro terá o diretório para cada pet.
  </li>
</ul>
