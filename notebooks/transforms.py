import random

# functionality-preserving transforms to perform against target scripts

def insert_cmdlet(script_text, length, chars, dashcount, insert_newline=False):
    """
    AstCmdletMetrics_CharacterDistribution_t_74_Percent                         0.0397031         10.671         2.27122
    AstCmdletMetrics_CharacterDistribution_e_65_Percent                         0.0272202         13.2826        3.27443
    AstCmdletMetrics_CharacterDistribution_o_6f_Percent                         0.00127544         5.38441       1.02836
    AstCmdletMetrics_CharacterDistribution_c_63_Percent                         0.000535396        3.13904       0.676892
    AstCmdletMetrics_CharacterDistribution_n_6e_Percent                         0.00049663         2.91592       0.484886
    AstCmdletMetrics_CharacterDistribution_t_74_Count                           0.00270285        26.478         5.58667
    AstCmdletMetrics_CharacterDistribution__2d_Count                            0.00128145        16.024         7.35733 (-)
    AstCmdletMetrics_CharacterDistribution_e_65_Count                           0.00115418        31.8927        7.812
    AstCmdletMetrics_CharacterDistribution_r_72_Count                           0.000865935       14.096         2.88467
    AstCmdletMetrics_CharacterDistribution_o_6f_Count                           0.000541578       14.478         3.67133
        t,e,r,o - c,n,t

    AstCmdletMetrics_Length_Median                                              0.00262015        11.094         5.35133
    AstCmdletMetrics_Length_Maximum                                             0.00175196        18.144        10.556
    AstCmdletMetrics_Length_Average                                             0.00166602        11.1502        5.56759
    
    use length - 6-18
    """

    cmdlet_string = ""
    
    if(isinstance(chars, str)):
        chars = [char for char in chars]
    
    for i in range(int(length/2)):
        cmdlet_string += random.choice(chars)
    
    for i in range(dashcount):
        cmdlet_string += "-"
    
    for i in range(int(length/2)):
        cmdlet_string += random.choice(chars)
    
    if(insert_newline):
        return f"function {cmdlet_string} {{}}; {cmdlet_string}\n{script_text}"
    else:
        return f"function {cmdlet_string} {{}}; {cmdlet_string};{script_text}"


def insert_string(script_text, var_length, var_chars, str_len, str_chars, insert_newline=False):
    """
    AstStringMetrics_Length_Average                                             0.0166362         35.5697        9.94479
    AstStringMetrics_Length_Minimum                                             0.00275039         9.88467       4.706
    AstStringMetrics_Length_Mode                                                0.00248716        24.0713        5.3
    AstStringMetrics_Length_Median                                              0.0021377         25.618         7.236
    AstStringMetrics_Length_Maximum                                             0.000311579      182.445       122.719
    AstStringMetrics_CharacterDistribution__5c_Percent                          0.000456682        1.00476       0.064064 (\)
    AstStringMetrics_CharacterDistribution_e_65_Percent                         0.000212224        7.89859       6.87804

    AstVariableNameMetrics_CharacterDistribution_r_72_Percent                   0.000664868        7.01397       4.51975
    AstVariableNameMetrics_CharacterDistribution_a_61_Count                     0.000227214       34.9793       26.344
    AstVariableNameMetrics_CharacterDistribution_e_65_Count                     0.000130424       67.1047       52.9473
    AstVariableNameMetrics_Length_Average                                       0.000312818       7.88717        9.5769

    LineByLineMetrics_CharacterDistribution_t_74_Percent                        0.00946966         5.60125       3.43217
    LineByLineMetrics_CharacterDistribution_i_69_Percent                        0.000629852        3.83979       2.45931
    LineByLineMetrics_CharacterDistribution_h_68_Percent                        0.000574188        1.24376       0.789021
    LineByLineMetrics_CharacterDistribution_s_73_Count                          0.000559488      138.099       108.877
    LineByLineMetrics_CharacterDistribution_l_6c_Percent                        0.000476667        2.43515       1.55726
    """
    
    var_string = "$"
    str_string = ""

    if(isinstance(var_chars, str)):
        var_chars = [char for char in var_chars]
    
    if(isinstance(str_chars, str)):
        str_chars = [char for char in str_chars]
    
    for i in range(var_length):
        var_string += random.choice(var_chars)
    
    for i in range(str_len):
        str_string += random.choice(str_chars)
    
    if insert_newline:
        return f"{var_string}=\"{str_string}\"\n{script_text}"
    else:
        return f"{var_string}=\"{str_string}\";{script_text}"


def insert_variable_member(script_text, var_length, var_chars, member_len, member_chars, insert_newline=False):
    """
    AstMemberMetrics_CharacterDistribution_t_74_Percent                         0.00960573         6.9418        2.1817
    AstMemberMetrics_CharacterDistribution_e_65_Percent                         0.00033005        10.5323        4.97794
    AstMemberMetrics_CharacterDistribution_o_6f_Percent                         0.000186795        5.16649       2.38709

    AstMemberMetrics_Length_Range                                               0.00111712        9.462         17.38
    AstMemberMetrics_Length_Maximum                                             0.000723824      13.764         23.4453
    AstMemberMetrics_Length_Average                                             0.000394764       7.78232       11.581

    AstVariableNameMetrics_CharacterDistribution_r_72_Percent                   0.000664868        7.01397       4.51975
    AstVariableNameMetrics_CharacterDistribution_a_61_Count                     0.000227214       34.9793       26.344
    AstVariableNameMetrics_CharacterDistribution_e_65_Count                     0.000130424       67.1047       52.9473
    AstVariableNameMetrics_Length_Average                                       0.000312818       7.88717        9.5769
    """

    var_string = "$"
    member_string = ""
    
    if(isinstance(var_chars, str)):
        var_chars = [char for char in var_chars]
    
    if(isinstance(member_chars, str)):
        member_chars = [char for char in member_chars]
        
    for i in range(var_length):
        var_string += random.choice(var_chars)
    
    for i in range(member_len):
        member_string += random.choice(member_chars)
    
    if insert_newline:
        return f"{var_string}.{member_string}\n{script_text}"
    else:
        return f"{var_string}.{member_string};{script_text}"




# # Misc:

# LineByLineMetrics_CharacterDistribution_t_74_Percent                        0.00946966         5.60125       3.43217
# LineByLineMetrics_CharacterDistribution_i_69_Percent                        0.000629852        3.83979       2.45931
# LineByLineMetrics_CharacterDistribution_h_68_Percent                        0.000574188        1.24376       0.789021
# LineByLineMetrics_CharacterDistribution_s_73_Count                          0.000559488      138.099       108.877
# LineByLineMetrics_CharacterDistribution_l_6c_Percent                        0.000476667        2.43515       1.55726
