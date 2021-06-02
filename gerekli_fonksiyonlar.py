



def control_df(df):
    print("###############################################################")
    print("İlk 5 veri")
    print(df.head())
    print("###############################################################")
    print("Verinin boyutları:")
    print(df.shape)
    print("###############################################################")
    print("Verideki boş gözlem sayısı:")
    print(df.isnull().sum())
    cat_cols = [col for col in df.columns if df[col].dtype == "O"]
    num_but_cat_cols = [col for col in df.columns if df[col].nunique() < 10 and df[col].dtype != "O"]
    cat_but_num_cols = [col for col in df.columns if df[col].nunique() > 20 and df[col].dtype == "O"]
    cat_cols = cat_cols + num_but_cat_cols
    num_cols = [col for col in df.columns if col not in cat_cols]
    print("###############################################################")
    print("Verideki kategorik değişkenler")
    print(cat_cols)
    print("###############################################################")
    print("Verideki sayısal değişkenler")
    print(num_cols)

    return cat_cols, num_cols


def cat_analysis(df,col_name,info=True):
    print(f"{col_name.capitalize()} adlı değişkenin gözlemlerinin yüzdesel oranı:")
    ratio=(df[col_name].value_counts()/len(df)*100)
    print(f"{ratio}")
    if info:
        print("info".center(50,"#"))
        print(df.groupby(col_name).mean())
        print("\n\n")


def compare_draw(df1,col1,target,df2=False,col2=False):
    plt.subplot(1,2,1)
    ss=df1.groupby(col1)[target].mean()
    plt.ylabel(col1)
    plt.title(f"{col1} adlı değişken kırılımında ortalama ücret")
    plt.legend()
    sns.barplot(x=ss.index,y=ss.values)
    plt.xticks(rotation=45)
    plt.show()
    print("\n")
    print(ss)
    print("######################\n\n")
    if type(df2) != bool :
        plt.subplot(1,2,2)
        ss=df2.groupby(col2)[target].mean()
        plt.ylabel(col2)
        plt.title(f"{col2} adlı değişken kırılımında ortalama ücret")
        plt.legend()
        plt.xticks(rotation=45)
        sns.barplot(x=ss.index,y=ss.values)
        plt.show()
        print("\n")
        print(ss)
        print("######################\n\n")


def user(region, child, smoker, age):
    if age < 22:
        age = "0_22"
    elif age >= 22 and age < 30:
        age = "22_30"
    elif age >= 30 and age < 45:
        age = "30_45"
    elif age >= 45 and age <= 70:
        age = "45_70"
    else:
        print("0-70 yaş aralığında bir sayı giriniz")

    s = region.upper() + "_" + str(child).upper() + "_" + smoker.upper() + "_" + age.upper()

    t = persona_df[persona_df["level_based"] == s]
    print(t)

    return


def missing_fill(df):
    ab = agg_df[agg_df["charges"].isnull()]
    for i in ab.index:
        if (ab["smoker"][i] == "no") and (ab["region"][i] == "northeast"):
            ab["charges"][i] = agg_df[(agg_df["smoker"] == "no") & (agg_df["region"] == "southeast") & (
                        agg_df["age_cat"] == ab["age_cat"][i])]["charges"].mean()

        elif (ab["smoker"][i] == "no") and (ab["region"][i] == "southeast"):
            ab["charges"][i] = agg_df[(agg_df["smoker"] == "no") & (agg_df["region"] == "northeast") & (
                        agg_df["age_cat"] == ab["age_cat"][i])]["charges"].mean()

        elif (ab["smoker"][i] == "no") and (ab["region"][i] == "northwest"):
            ab["charges"][i] = agg_df[(agg_df["smoker"] == "no") & (agg_df["region"] == "southwest") & (
                        agg_df["age_cat"] == ab["age_cat"][i])]["charges"].mean()

        elif (ab["smoker"][i] == "no") and (ab["region"][i] == "southwest"):
            ab["charges"][i] = agg_df[(agg_df["smoker"] == "no") & (agg_df["region"] == "northwest") & (
                        agg_df["age_cat"] == ab["age_cat"][i])]["charges"].mean()

        elif (ab["smoker"][i] == "yes") and (ab["region"][i] == "northeast"):
            ab["charges"][i] = agg_df[(agg_df["smoker"] == "yes") & (agg_df["region"] == "southeast") & (
                        agg_df["age_cat"] == ab["age_cat"][i])]["charges"].mean()

        elif (ab["smoker"][i] == "yes") and (ab["region"][i] == "southeast"):
            ab["charges"][i] = agg_df[(agg_df["smoker"] == "yes") & (agg_df["region"] == "northeast") & (
                        agg_df["age_cat"] == ab["age_cat"][i])]["charges"].mean()

        elif (ab["smoker"][i] == "yes") and (ab["region"][i] == "northwest"):
            ab["charges"][i] = agg_df[(agg_df["smoker"] == "yes") & (agg_df["region"] == "southwest") & (
                        agg_df["age_cat"] == ab["age_cat"][i])]["charges"].mean()

        elif (ab["smoker"][i] == "yes") and (ab["region"][i] == "southwest"):
            ab["charges"][i] = agg_df[(agg_df["smoker"] == "yes") & (agg_df["region"] == "northwest") & (
                        agg_df["age_cat"] == ab["age_cat"][i])]["charges"].mean()

    return ab