# house-rocket-production
This repository contains python code and scripts from a dummy data science project of type Insights

# House Rocket Company
[![NPM](https://img.shields.io/npm/l/react)](https://github.com/devsuperior/sds1-wmazoni/blob/master/LICENSE) 

# Sobre o projeto

https://analyse-house-rocket.herokuapp.com/

<p>Este é um projeto para fins de estudo, em uma empresa ficticia, onde o contexto e as perguntas de negócios não são reais e não têm objetivo comercial. A base de dados é de domínio público e está disponivel no portal <a href="https://www.kaggle.com/harlfoxem/housesalesprediction" rel="nofollow">Kaggle</a>.</p>


# O problema de negócio

A House Rocket é uma plataforma digital em que o Core de negócio se trata da compra e a venda de imóveis usando portal de vendas on-line. A alta gestão da empresa solicitou um projeto de análise de dados com o objetivo de maximizar a receita da empresa encontrando boas oportunidades de negócio. Sua principal estratégia é comprar boas casas em ótimas localizações com preços baixos e depois revendê-las posteriormente à preços mais altos, aumentando o lucro da empresa e, portanto, a sua receita.

## Layout do projeto
#### Visualização geral e descrições estatísticas
![Web 1](https://github.com/JulianoRRamos/house-rocket-production/blob/2e102dadee53f0a9c22c379804fdbf29975dfe70/images/Layout1.png)

#### Mapa de densidade de portifólio e gráfico de evolução de preço por ano
![Web 2](https://github.com/JulianoRRamos/house-rocket-production/blob/2e102dadee53f0a9c22c379804fdbf29975dfe70/images/Layout2.png)

#### Distribuição de casas do portifólio por números de quartos, banheiros, andares, vista para o mar
![Web 3](https://github.com/JulianoRRamos/house-rocket-production/blob/2e102dadee53f0a9c22c379804fdbf29975dfe70/images/Layout3.png)
## 1. Oportunidades:
O objetivo do projeto é encontrar, através de Insights gerados por Análise Exploratória de Dados (EDA), oportunidades de negócios na região de portifólio da empresa House Rocket.

## 2. Necessidades de Negócio:

- Dificuldade do time do negócios para tomar boas decisões de compra com as informações que possuem atualmente.
- Por possuir um portfólio grande, realizar o trabalho manualmente demandaria muito tempo.

- Principais questões respondidas:
  - Quais são os imóveis que deveríamos comprar?
  - Uma vez o imóvel comprado, qual o melhor momento para vendê-lo, e por qual preço?
  - A House Rocket deveria fazer uma reforma para aumentar o preço da venda? Quais seriam as sugestões de mudanças? Qual o incremento no preço dado por cada opção de reforma?

## 3. Requisitos:

### 3.1 Acesso a solução: 
  Os produtos gerados serão acessados pela internet em 24/7. 
### 3.2 Validações: 
  O planejamento será validados com as equipes de negócio para confirmação de valores agregados nas tomadas de decisão da empresa.
### 3.3 Origem dos dados: 
  A base de dados coletada on-line no portal <a href="https://www.kaggle.com/harlfoxem/housesalesprediction" rel="nofollow">Kaggle</a> contem os seguintes atributos de dados:

<table>
<thead>
<tr>
<th>Variável</th>
<th>Definição</th>
</tr>
</thead>
  <tbody>
<tr>
<td>id</td>
<td>Identificador de cada imóvel.</td>
</tr>
<tr>
<td>date</td>
<td>Data em que a imóvel ficou disponível.</td>
</tr>
<tr>
<td>price</td>
<td>O preço de cada imóvel, considerado como preço de compra.</td>
</tr>
<tr>
<td>bedrooms</td>
<td>Número de quartos.</td>
</tr>
<tr>
<td>bathrooms</td>
<td>O número de banheiros, o valor 0,5 indica um quarto com banheiro, mas sem chuveiro. O valor 0,75 ou 3/4 banheiro representa um banheiro que contém uma pia, um vaso sanitário e um chuveiro ou banheira.</td>
</tr>
<tr>
<td>sqft_living</td>
<td>Pés quadrados do interior das casas.</td>
</tr>
<tr>
<td>sqft_lot</td>
<td>Pés quadrados do terreno das casas.</td>
</tr>
<tr>
<td>floors</td>
<td>Número de andares.</td>
</tr>
<tr>
<td>waterfront</td>
<td>Uma variável fictícia para saber se a casa tinha vista para a orla ou não, '1' se o imóvel tem uma orla, '0' se não.</td>
</tr>
<tr>
<td>view</td>
<td>Vista, Um índice de 0 a 4 de quão boa era a visualização da imóvel.</td>
</tr>
<tr>
<td>condition</td>
<td>Um índice de 1 a 5 sobre o estado das moradias, 1 indica imóvel degradado e 5 excelente.</td>
</tr>
<tr>
<td>grade</td>
<td>Uma nota geral é dada à unidade habitacional com base no sistema de classificação de King County. O índice de 1 a 13, onde 1-3 fica aquém da construção e design do edifício, 7 tem um nível médio de construção e design e 11-13 tem um nível de construção e design de alta qualidade.</td>
</tr>
<tr>
<td>sqft_above</td>
<td>Os pés quadrados do espaço habitacional interior acima do nível do solo.</td>
</tr>
<tr>
<td>sqft_basement</td>
<td>Os pés quadrados do espaço habitacional interior abaixo do nível do solo.</td>
</tr>
<tr>
<td>yr_built</td>
<td>Ano de construção da imóvel.</td>
</tr>
<tr>
<td>yr_renovated</td>
<td>Representa o ano em que o imóvel foi reformado. Considera o número ‘0’ para descrever as imóvel nunca renovadas.</td>
</tr>
<tr>
<td>zipcode</td>
<td>Um código de cinco dígitos para indicar a área onde se encontra a imóvel.</td>
</tr>
<tr>
<td>lat</td>
<td>Latitude.</td>
</tr>
<tr>
<td>long</td>
<td>Longitude.</td>
</tr>
<tr>
<td>sqft_living15</td>
<td>O tamanho médio em pés quadrados do espaço interno de habitação para as 15 casas mais próximas.</td>
</tr>
<tr>
<td>sqft_lot15</td>
<td>Tamanho médio dos terrenos em metros quadrados para as 15 casas mais próximas.</td>
</tr>    
 </tbody>
</table>

## 4. Planejamento da solução:

### 4.1 Produtos gerados:
Dashboard interativo do portfólio disponível, com todas informações mais relevantes disponíveis atualmente, para que o CEO e o time de negócios possa realizar análises (self-service BI).

### 4.2 Ferramentas utilizadas:
- Linguagem de programação: Python.
- IDE/Compiladores: Jupyter Notebook, Pycharm.
- Repositório: Git / Github.
- Tecnologia de apresentação: Geopandas, Streamlit.
- Serviço de Publicação: Heroku.

## 5. Insights principais:

### 5.1 xxxxx.
### 5.2 yyyyy.
### 5.3 wwww.

## Autor

Juliano Rodrigues Ramos

https://www.linkedin.com/in/juliano-rodrigues-ramos-73b07146/

<h2 dir="auto"><a id="user-content-6-referências" class="anchor" aria-hidden="true" href="#6-referências"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z"></path></svg></a>6 Referências</h2>
<ul dir="auto">
<li>
<p dir="auto">Este projeto é um dos desafios de implementação durante os cursos da <a href="https://www.comunidadedatascience.com/" rel="nofollow">Comunidade DS</a>.</p>
</li>
<li>
<p dir="auto">O Dataset foi obtido no repositório público: <a href="https://www.kaggle.com/harlfoxem/housesalesprediction" rel="nofollow">Kaggle</a>.</p>
</li>
<li>
<p dir="auto">Os dados geoespaciais foram obtidos no <a href="https://geodacenter.github.io/data-and-lab/KingCounty-HouseSales2015/" rel="nofollow">Geocenter</a>.</p>
</li>
</ul>
