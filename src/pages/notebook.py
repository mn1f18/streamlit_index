import streamlit as st
import random

def show():


    # Game introduction
    st.title("石头、剪刀、布游戏")
    st.write("请选择：石头、剪刀、布!")
    user_choice = ""
    # User's choice
    s
    if  st.button("石头"):
        user_choice = "石头"
    if  st.button("剪刀"):
        user_choice = "剪刀"
    if  st.button("布"):
        user_choice = "布"
    # Computer's choice
    choices = ["石头", "剪刀", "布"]
    computer_choice = random.choice(choices)

    # Button to play the game
    if user_choice =="石头"or "剪刀"or"布":
        st.write(f"电脑选择了: {computer_choice}")
        
        # Determine winner
        if user_choice == computer_choice:
            st.write("平局！")
        elif (user_choice == "石头" and computer_choice == "剪刀") or \
            (user_choice == "剪刀" and computer_choice == "布") or \
            (user_choice == "布" and computer_choice == "石头"):
            st.write("你赢了！")
        else:
            st.write("你输了！")
