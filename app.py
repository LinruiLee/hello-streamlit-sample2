import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as sci
from pandas import DataFrame
from PIL import Image
import numpy as np
from matplotlib.patches import Circle, Rectangle, Arc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from matplotlib.colors import ListedColormap

def main():
    st.markdown("<h1 style= 'text-align: center; color: black;'>库里投篮可视化分析及机器学习</h1>", unsafe_allow_html= True)
    st.markdown("<h3 style= 'text-align: center; color: red;'>庆祝 史蒂芬库里 登顶NBA三分王</h3>",unsafe_allow_html=True)
    st.markdown('*By HandsomeLee*')
    img = Image.open("SZULOGO.jpg")
    st.image(img, width= 400)

    st.subheader("球员数据比较可视化")

    def file_selector(folder_path= 'drafts_datas'):
        filenames = os.listdir(folder_path)
        selected_filename = st.selectbox("库里选秀上下届、同届的2008-10年nba新秀数据", filenames)
        return os.path.join(folder_path, selected_filename)

    filename = file_selector()
    df = pd.read_csv(filename)
    df1 = pd.read_csv('./drafts_datas/drafts_2003-18.csv')



    if st.checkbox("选择准备分析的数据"):

        all_columns = df.columns.tolist()
        del all_columns[0:3]
        selected_columns = st.multiselect("选择数据项目", all_columns)
        data_select = df[selected_columns]
        data_select_df = DataFrame(data_select)
        concat_df = pd.concat([data_select_df], axis= 1)
        new_columns_player = df.Player
        concat_df.index = [new_columns_player]
        st.dataframe(concat_df)

    #Plot an Visualzation

        type_of_plot = st.selectbox("可视化类型(热力图、密度图、热图、非线性回归图、分类散点图、矩阵散点图)",["热力图", "密度图(限两个变量集)", "热图(限一个变量集)", "非线性回归图(限两个变量集)", "分类散点图(限一个变量集)", "矩阵散点图"])
        if st.button('生成可视化图'):
            if type_of_plot == "热力图":
                area_data = df[selected_columns]
                st.area_chart(area_data)
            elif type_of_plot == "密度图(限两个变量集)":
                plt.scatter(concat_df.iloc[:, 3:4], concat_df.iloc[:, 4:5])
                kde_plot = sns.jointplot(concat_df.iloc[:, 3:4], concat_df.iloc[:, 4:5], concat_df, color = 'k', stat_func=sci.pearsonr, kind = 'kde', size= 8, shade_lowest = False)
                kde_plot.plot_joint(plt.scatter, c = 'w', s = 10, linewidth = 1, marker = '+')
                st.write(kde_plot)
                st.pyplot()
            elif type_of_plot == "热图(限一个变量集)":
                x = concat_df.iloc[:, 0:1]
                y = concat_df.iloc[:, 2:3]
                z = concat_df.iloc[:, 3:4]
                heatmap_df = pd.concat([x, y, z], axis=1)
                #heatmap_df_columns = heatmap_df.Year
                #heatmap_df.index = [heatmap_df_columns]
                #尝试删去2003-2012年的新秀数据heatmap_df = heatmap_df[-heatmap_df.Year.isin([2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012])]
                heatmap_df.columns = ['Year', 'Round', 'Selected']
                heatmap_df.reset_index(drop= True, inplace= True)
                #按year和round进行分组索引后得到的聚合数据(由于通过groupby()函数分组得到的是一个DataFrameGroupBy对象)
                # 再用['Selected'].agg重新输出成dataframe格式,mean是取分组均值
                #as_index= False可以不改变原有index,把year和round两组的数据只暂时缓存为索引index
                heatmap_df = heatmap_df.groupby(['Year', 'Round'], as_index= False)['Selected'].agg('mean')
                heatmap_df = heatmap_df.pivot('Year', 'Round', 'Selected')
                st.dataframe(heatmap_df.head())
                heatmap_plot = sns.heatmap(heatmap_df, annot= True, cmap= 'Reds', cbar= True)
                st.write(heatmap_plot)
                st.pyplot()
            elif type_of_plot == "非线性回归图(限两个变量集)":
                x = concat_df.iloc[:, 3:4]
                y = concat_df.iloc[:, 4:5]
                reg_df = pd.concat([x, y], axis= 1)
                reg_df.columns = ['Selected1', 'Selected2']
                reg_plot = sns.lmplot(x= 'Selected1', y='Selected2', data= reg_df, order= 4)
                st.write(reg_plot)
                st.pyplot()
            elif type_of_plot == "分类散点图(比较乐透和非乐透球员,限一个变量集)":
                x = concat_df.iloc[:, 0:1]
                y = concat_df.iloc[:, 1:2]
                z = concat_df.iloc[:, 3:4]
                strip_df = pd.concat([x, y, z], axis= 1)
                strip_df.columns = ['Year', 'Category', 'Selected']
                sns.stripplot(x= 'Year', y= 'Selected', data= strip_df, jitter= 0.1, size= 5, edgecolor= 'w', linewidth= 1, marker= 'o')
                strip_plot = sns.stripplot(x= 'Category', y= 'Selected', hue= 'Year', data=strip_df, jitter= True)
                st.write(strip_plot)
                st.pyplot()
            elif type_of_plot == "矩阵散点图(三个或四个变量集最佳)":
                z = concat_df.iloc[:, 2:3]
                xy = concat_df.iloc[:, 3:]
                matrix_df = pd.concat([z, xy], axis= 1)
                matrix_plot = sns.pairplot(matrix_df, kind='scatter', diag_kind= 'hist', hue= 'Round', palette= 'husl', size= 3)
                st.write(matrix_plot)
                st.pyplot()

    st.subheader("投篮热图")

    html_temp = """
    <div style= "background-color:tomato;"><p style="color: white; font-size: 15px;">请于左侧选择库里上下届、同届的明星球员:</p></div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    
    def shot_selector(folder_path= './player_shotchart_datas'):
        filenames = os.listdir(folder_path)
        selected_filename = st.sidebar.selectbox("球员", filenames)
        return os.path.join(folder_path, selected_filename)

    shot_filename = shot_selector()
    shot_df = pd.read_csv(shot_filename)

    if st.checkbox("球员投篮热图"):


        def draw_court(ax=None, color='black', lw=2, outer_lines=False):
            # If an axes object isn't provided to plot onto, just get current one
            if ax is None:
                ax = plt.gca()

            # Create the various parts of an NBA basketball court

            # Create the basketball hoop
            # Diameter of a hoop is 18" so it has a radius of 9", which is a value
            # 7.5 in our coordinate system
            hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

            # Create backboard
            backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

            # The paint
            # Create the outer box 0f the paint, width=16ft, height=19ft
            outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                                fill=False)
            # Create the inner box of the paint, widt=12ft, height=19ft
            inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                                fill=False)

            # Create free throw top arc
            top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                                linewidth=lw, color=color, fill=False)
            # Create free throw bottom arc
            bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                                    linewidth=lw, color=color, linestyle='dashed')
            # Restricted Zone, it is an arc with 4ft radius from center of the hoop
            restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                            color=color)

            # Three point line
            # Create the side 3pt lines, they are 14ft long before they begin to arc
            corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                                    color=color)
            corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
            # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
            # I just played around with the theta values until they lined up with the 
            # threes
            three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                            color=color)

            # Center Court
            center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                                linewidth=lw, color=color)
            center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                                linewidth=lw, color=color)

            # List of the court elements to be plotted onto the axes
            court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                            bottom_free_throw, restricted, corner_three_a,
                            corner_three_b, three_arc, center_outer_arc,
                            center_inner_arc]

            if outer_lines:
                # Draw the half court line, baseline and side out bound lines
                outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                        color=color, fill=False)
                court_elements.append(outer_lines)

            # Add the court elements onto the axes
            for element in court_elements:
                ax.add_patch(element)

            return ax

        plt.figure(figsize=(12,11))
        plt.scatter(shot_df.LOC_X, shot_df.LOC_Y)
        draw_court()
        plt.xlim(-250,250)
        plt.ylim(422.5, -47.5)
        # get rid of axis tick labels
        # plt.tick_params(labelbottom=False, labelleft=False)
        st.pyplot()

    st.subheader("机器学习及预测")
    st.markdown("选取球员的两个属性，经过随机抽取训练集样本完成模型训练后，预测球员是否为乐透球员")
    html_temp = """
    <div style= "background-color:tomato;"><p style="color: white; font-size: 15px;">在drafts_2003-18新秀样本中,以您选择的Selected1和Selected2为两个自变量集</p></div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    if st.checkbox("请选择两个变量"):
        l_Category = df1.loc[:, ['Category']]
        l_Category.loc[l_Category['Category']== 'Lottery Players'] = 1
        l_Category.loc[l_Category['Category']== 'Non-lottery Players'] = 0
        l_all_columns = df1.columns.tolist()
        del l_all_columns[0:8]
        l_selected_columns = st.multiselect("Select data", l_all_columns)
        l_data_select = df1[l_selected_columns]
        l_data_select_df = DataFrame(l_data_select)
        l_concat_df = pd.concat([l_Category, l_data_select_df], axis= 1)
        l_concat_df.dropna(axis= 0, how= 'any', inplace= True)#删除NAN数据
        if st.button("机器学习logistic Regression预测"):
            X = l_concat_df.iloc[:, 1:].astype('str').values
            Y = l_concat_df.iloc[:, 0].astype('str').values

            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.25, random_state = 0)
            #Feature Scaling特征缩放 

            sc_X = StandardScaler()
            X_train = sc_X.fit_transform(X_train)
            X_test = sc_X.transform(X_test)
            #Fitting Logistic Regression to the Training set

            classifier = LogisticRegression(random_state = 0)
            classifier.fit(X_train, Y_train)
            #Predicting the Test set results
            Y_pred = classifier.predict(X_test)
            #Making the Confusion Matrix 混淆矩阵评估性能

            cm = confusion_matrix(Y_test,Y_pred)
            st.table(cm)
            a = cm[0, 0]
            b = cm[1, 1]
            c = cm[0, 1]
            d = cm[1, 0]
            cm_result = int((a+b)/(a+b+c+d)*100)
            st.info("您选择了以{}为Selected1,Selected2自变量集".format(l_selected_columns))
            st.success('预测成功率为{}%'.format(cm_result))
            #Visualing

            X_set, Y_set = X_train, Y_train
            X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                                np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
            plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
                        alpha = 0.75, cmap = ListedColormap(('red', 'green')))
            plt.xlim(X1.min(), X1.max())
            plt.ylim(X2.min(), X2.max())
            for i, j in enumerate(np.unique(Y_set)):
                plt.scatter(X_set[Y_set == j, 0], X_set[Y_set == j, 1],
                            c = ListedColormap(('orange', 'blue'))(i), label = j)
            plt.title('Classifier (Training set)')
            plt.xlabel('Selected1(Feature Scaling)')#selected1
            plt.ylabel('Selected2(Feature Scaling)')#selected2
            plt.legend()
            st.pyplot()

            X_set, Y_set = X_test, Y_test
            X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                                np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
            plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
                        alpha = 0.75, cmap = ListedColormap(('red', 'green')))
            plt.xlim(X1.min(), X1.max())
            plt.ylim(X2.min(), X2.max())
            for i, j in enumerate(np.unique(Y_set)):
                plt.scatter(X_set[Y_set == j, 0], X_set[Y_set == j, 1],
                            c = ListedColormap(('orange', 'blue'))(i), label = j)
            plt.title('Classifier (Test set)')
            plt.xlabel('Selected1(Feature Scaling)')
            plt.ylabel('Selected2(Feature Scaling)')
            plt.legend()
            st.pyplot()

if __name__ == "__main__":
    main()
