import requests
import sys
import streamlit as st


# Gets the contents of an image on the Internet to be
# sent to the machine learning model for classifying
def getImageUrlData(wwwLocationOfImage):
    data = requests.get(wwwLocationOfImage).content
    if sys.version_info[0] < 3:
        # Python 2 approach to handling bytes
        return data.encode("base64")
    else:
        # Python 3 approach to handling bytes
        import base64
        return base64.b64encode(data).decode()


# This function will pass your image to the machine learning model
# and return the top result with the highest confidence
def classify(imageurl):
    key = "8919f4b0-2280-11eb-9ffb-71e2cfe99e113f0b5ae3-0f0e-49da-be1f-13a3bc8cb55b"
    url = "https://machinelearningforkids.co.uk/api/scratch/" + key + "/classify"

    response = requests.post(url, json={"data": getImageUrlData(imageurl)})

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()


st.title('what the cover of your favorite album says about it?')
st.subheader('“ Without music, life would be a mistake."')
st.subheader('― Friedrich Nietzsche, Twilight of the Idols')
st.header(
    'Olá, quer saber, apenas pela capa do seu álbum favorito, se ele se parece mais com um álbum triste, feliz, '
    'clássico ou '
    'progressivo? Coloque '
    'aqui '
    'o endereço de imagem dele e descubra!')

user_input = st.text_area("Insira o endereço de imagem do álbum aqui")
if st.button('Enviar'):
    result = user_input
    demo = classify(result)

    label = demo["class_name"]
    confidence = demo["confidence"]
    st.balloons()

    # CHANGE THIS to do something different with the result
    st.success("Aqui estão os resultados:")
    st.image([user_input], width=300)

    if confidence < 70:
        st.write("Talvez isso não seja uma capa de um álbum ou seu álbum é muito incrível para ser rotulado em apenas "
                 "uma dessas categorias. Tente outra imagem!")
    elif label == 'sad':
        st.write("Olá pessoa que gosta de sofrer. Temos %d%% de certeza que esse álbum contém músicas tristes."
                 " Então se estiver em um dia ruim, ou não, e quiser apenas relaxar com algo meio melancólico sobre "
                 "relacionamentos, vida ou alguma situação, apenas escute." % confidence)
        st.info("Se você gosta desse álbum recomendamos: AM, de Arctic Monkeys, Is This It, de The Strokes e "
                "Ultraviolence, de Lana Del Rey na parte internacional e qualquer álbum de Jorge e Mateus, Henrique e "
                "Juliano e Marilia Mendonça na parte nacional ")
    elif label == 'progressive':
        st.write("Olha o que temos aqui!!! Pela capa do seu álbum, temos %d%% de certeza que ele se trata de um álbum "
                 "progressivo ou que pelo menos algumas de suas músicas são. A música progressiva expande as "
                 "fronteiras estilísticas existentes associadas a gêneros musicais específicos, ou seja, suas músicas "
                 "são tão diferentes e especiais como a capa do seu álbum. Tenha uma boa apreciação." % confidence)

        st.info("Se você gosta desse álbum recomendamos: qualquer álbum do Pink Floyd se você busca algo "
                "internacional e quaquer uma do Boogarins se você quer algo nacional.")
    elif label == 'happy':
        st.write("Feliz como você! Artisticamente falando, e com %d%% de confiança, esse parece ser um álbum com "
                 "músicas majoritariamente "
                 "felizes. Então se você precisa dar uma animada, a hora de escutar esse álbum é agora! " % confidence)

        st.info("Se você gosta desse álbum recomendamos: Loud, de Rihanna, O Tempo é Agora, de Anavitória e Dança "
                "Entre Casais, de Jovem Dionisio")
    elif label == 'classic':
        st.write("A comunidade clássica está em festa!! Pela capa desse álbum, garantimos em %d%% de certeza que se "
                 "trata de um "
                 "álbum clássico. "
                 "Melodias originais, eternas e sensitivas o/a esperam. Aprecie ao máximo." % confidence)

        st.info("Se você gosta desse álbum recomendamos: Classical Sunday, de Ludwig Van Beethoven, Tchaikovsky suite "
                "no. 4, de Piotr Ilitch Tchaikovsk e Making Out To Mozart, de Wolfgang Amadeus Mozart")

