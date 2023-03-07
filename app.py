import streamlit as st
from PIL import Image
import os
from datetime import datetime

st.set_page_config(layout="wide")

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

upload_image = st.file_uploader('', type=['jpg','png','jpeg'])
background_r = None
img_save_dir = ""
col1, col2 = st.columns(2)

with col1:
    # holder = st.empty()
    # upload_image = holder.file_uploader('', type=['jpg','png'])
    
    if upload_image != None:
        date_now = str(datetime.now())[0:19].replace('-','_').replace(' ','_').replace(':',"_")
        background = Image.open("./img/back_upper.jpg")
        foreground = Image.open(upload_image)
        
        img_save_dir = './fast-style-transfer/input/img_' + date_now + ".jpg"
        output_img_dir = img_save_dir.replace("/input/","/output/")
        
        foreground.save(img_save_dir, 'JPEG')
        b_h, b_w = background.size
        f_h, f_w = foreground.size
        ## foreground가 background 보다 클 경우 처리해야 함
        background.paste(foreground,(int(b_h/2 - f_h/2),int(b_w/2 - f_w/2)))
        st.image(background)
        
        
    else:
        st.image("./img/back_upper.jpg")

    # version_opt = ["version1(▲stylization, ▼robustness)","version2(▲robustness, ▼stylization)"]
    version_opt = ["version1","version2"]
    version = st.radio(label = "version",
                        options = version_opt,
                        horizontal=True)
    
    if version == "version1":
        ckpt_dir = " ./fast-style-transfer/ckpt/style_image_9_ckpt "
    
    elif version == "version2":
        ckpt_dir = " ./fast-style-transfer/ckpt/style_image_13_ckpt "
    
    if img_save_dir != "":
        command = "python3 ./fast-style-transfer/evaluate.py " \
                            + "--checkpoint" + ckpt_dir \
                            + "--in-path " + img_save_dir \
                            + " --out-path " + output_img_dir
    else:
        pass
    
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        if st.button("클리어"):
            background_r = None
            
            input_dir = './fast-style-transfer/input'
            for f in os.listdir(input_dir):
                os.remove(os.path.join(input_dir, f))
            
            output_dir = './fast-style-transfer/output'
            for f in os.listdir(output_dir):
                os.remove(os.path.join(output_dir, f))
    
    with col1_2:
        if st.button("제출하기"):      
            
            print(command)
            os.system(command)
            background_r = Image.open("./img/back_right.jpg")
            foreground_r = Image.open(output_img_dir)

            b_r_h, b_r_w = background_r.size
            f_r_h, f_r_w = foreground_r.size
            ## foreground가 background 보다 클 경우 처리해야 함
            background_r.paste(foreground_r,(int(b_r_h/2 - f_r_h/2),int(b_r_w/2 - f_r_w/2)))
            

    # if st.button("clear"):
    #     st.experimental_rerun()
    # st.image("back_left.jpg")

    st.image("./img/back_left_bottom.jpg")

with col2:
    if background_r != None:
        st.image(background_r)
    else:
        st.image("./img/back_right.jpg")
    

