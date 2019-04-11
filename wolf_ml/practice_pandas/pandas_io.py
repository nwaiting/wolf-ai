#coding=utf-8


"""
    Pandas I/O API是一套像pd.read_csv()一样返回Pandas对象的顶级读取器函数
    读取文本文件(或平面文件)的两个主要功能是read_csv()和read_table()，它们都使用相同的解析代码来智能地将表格数据转换为DataFrame对象

    to_csv和read_csv：
        to_csv()是DataFrame类的方法，read_csv()是pandas的方法


    read_csv方法定义：
        pandas.read_csv(filepath_or_buffer, sep=', ', delimiter=None, header='infer', names=None,
                    index_col=None, usecols=None, squeeze=False, prefix=None, mangle_dupe_cols=True, dtype=None,
                    engine=None, converters=None, true_values=None, false_values=None, skipinitialspace=False,
                    skiprows=None, nrows=None, na_values=None, keep_default_na=True, na_filter=True, verbose=False,
                    skip_blank_lines=True, parse_dates=False, infer_datetime_format=False, keep_date_col=False,
                    date_parser=None, dayfirst=False, iterator=False, chunksize=None, compression='infer',
                    thousands=None, decimal=b'.', lineterminator=None, quotechar='"', quoting=0, escapechar=None,
                    comment=None, encoding=None, dialect=None, tupleize_cols=None, error_bad_lines=True,
                    warn_bad_lines=True, skipfooter=0, skip_footer=0, doublequote=True, delim_whitespace=False,
                    as_recarray=None, compact_ints=None, use_unsigned=None, low_memory=True, buffer_lines=None,
                    memory_map=False, float_precision=None

        常用参数：
            filepath_or_buffer : str，pathlib。str, pathlib.Path, py._path.local.LocalPath or any object with a read() method (such as a file handle or StringIO)
                                可以是URL，可用URL类型包括：http, ftp, s3和文件。对于多文件正在准备中
                                本地文件读取实例：://localhost/path/to/table.csv
            sep : str, default ‘,’
                    指定分隔符。如果不指定参数，则会尝试使用逗号分隔。分隔符长于一个字符并且不是‘\s+’,将使用python的语法分析器。并且忽略数据中的逗号。正则表达式例子：’\r\t’
            delimiter : str, default None
                    定界符，备选分隔符（如果指定该参数，则sep参数失效）
            delim_whitespace : boolean, default False.
                        指定空格(例如’ ‘或者’ ‘)是否作为分隔符使用，等效于设定sep=’\s+’。如果这个参数设定为Ture那么delimiter 参数失效。
                        在新版本0.18.1支持
            header : int or list of ints, default ‘infer’
                    指定行数用来作为列名，数据开始行数。如果文件中没有列名，则默认为0，否则设置为None。如果明确设定header=0 就会替换掉原来存在列名。header参数可以是一个list例如：[0,1,3]，这个list表示将文件中的这些行作为列标题（意味着每一列有多个标题），介于中间的行将被忽略掉（例如本例中的2；本例中的数据1,2,4行将被作为多级标题出现，第3行数据将被丢弃，dataframe的数据从第5行开始。）。
                    注意：如果skip_blank_lines=True 那么header参数忽略注释行和空行，所以header=0表示第一行数据而不是文件的第一行。
            names : array-like, default None
                    用于结果的列名列表，如果数据文件中没有列标题行，就需要执行header=None。默认列表中不能出现重复，除非设定参数mangle_dupe_cols=True。
            index_col : int or sequence or False, default None
                    用作行索引的列编号或者列名，如果给定一个序列则有多个行索引。
                    如果文件不规则，行尾有分隔符，则可以设定index_col=False 保证pandas用第一列作为行索引。
            usecols : array-like, default None
                    返回一个数据子集，该列表中的值必须可以对应到文件中的位置（数字可以对应到指定的列）或者是字符传为文件中的列名。例如：usecols有效参数可能是 [0,1,2]或者是 [‘foo’, ‘bar’, ‘baz’]。使用这个参数可以加快加载速度并降低内存消耗。
            as_recarray : boolean, default False
                    不赞成使用：该参数会在未来版本移除。请使用pd.read_csv(…).to_records()替代。
                    返回一个Numpy的recarray来替代DataFrame。如果该参数设定为True。将会优先squeeze参数使用。并且行索引将不再可用，索引列也将被忽略。
            squeeze : boolean, default False
                    如果文件值包含一列，则返回一个Series
            prefix : str, default None
                    在没有列标题时，给列添加前缀。例如：添加‘X’ 成为 X0, X1, …
            mangle_dupe_cols : boolean, default True
                    重复的列，将‘X’…’X’表示为‘X.0’…’X.N’。如果设定为false则会将所有重名列覆盖。
            dtype : Type name or dict of column -> type, default None
                    每列数据的数据类型。例如 {‘a’: np.float64, ‘b’: np.int32}
            engine : {‘c’, ‘python’}, optional
                    Parser engine to use. The C engine is faster while the python engine is currently more feature-complete.
                    使用的分析引擎。可以选择C或者是python。C引擎快但是Python引擎功能更加完备。
            converters : dict, default None
                    列转换函数的字典。key可以是列名或者列的序号。
            true_values : list, default None
                    Values to consider as True
            false_values : list, default None
                    Values to consider as False
            skipinitialspace : boolean, default False
                    忽略分隔符后的空白（默认为False，即不忽略）.
            skiprows : list-like or integer, default None
                    需要忽略的行数（从文件开始处算起），或需要跳过的行号列表（从0开始）。
            skipfooter : int, default 0
                    从文件尾部开始忽略。 (c引擎不支持)
            skip_footer : int, default 0
                    不推荐使用：建议使用skipfooter ，功能一样。
            nrows : int, default None
                    需要读取的行数（从文件头开始算起）。
            na_values : scalar, str, list-like, or dict, default None
                    一组用于替换NA/NaN的值。如果传参，需要制定特定列的空值。默认为‘1.#IND’, ‘1.#QNAN’, ‘N/A’, ‘NA’, ‘NULL’, ‘NaN’, ‘nan’`.
            keep_default_na : bool, default True
                    如果指定na_values参数，并且keep_default_na=False，那么默认的NaN将被覆盖，否则添加。
            na_filter : boolean, default True
                    是否检查丢失值（空字符串或者是空值）。对于大文件来说数据集中没有空值，设定na_filter=False可以提升读取速度。
            verbose : boolean, default False
                    是否打印各种解析器的输出信息，例如：“非数值列中缺失值的数量”等。
            skip_blank_lines : boolean, default True
                    如果为True，则跳过空行；否则记为NaN。
            parse_dates : boolean or list of ints or names or list of lists or dict, default False
            infer_datetime_format : boolean, default False
                    如果设定为True并且parse_dates 可用，那么pandas将尝试转换为日期类型，如果可以转换，转换方法并解析。在某些情况下会快5~10倍。
            keep_date_col : boolean, default False
                    如果连接多列解析日期，则保持参与连接的列。默认为False。
            date_parser : function, default None
                    用于解析日期的函数，默认使用dateutil.parser.parser来做转换。Pandas尝试使用三种不同的方式解析，如果遇到问题则使用下一种方式。
                    1.使用一个或者多个arrays（由parse_dates指定）作为参数；
                    2.连接指定多列字符串作为一个列作为参数；
                    3.每行调用一次date_parser函数来解析一个或者多个字符串（由parse_dates指定）作为参数。
            dayfirst : boolean, default False
                    DD/MM格式的日期类型
            iterator : boolean, default False
                    返回一个TextFileReader 对象，以便逐块处理文件。
            chunksize : int, default None
                    文件块的大小， See IO Tools docs for more informationon iterator and chunksize.
            compression : {‘infer’, ‘gzip’, ‘bz2’, ‘zip’, ‘xz’, None}, default ‘infer’
                    直接使用磁盘上的压缩文件。如果使用infer参数，则使用 gzip, bz2, zip或者解压文件名中以‘.gz’, ‘.bz2’, ‘.zip’, or ‘xz’这些为后缀的文件，否则不解压。如果使用zip，那么ZIP包中国必须只包含一个文件。设置为None则不解压。
                    新版本0.18.1版本支持zip和xz解压
            thousands : str, default None
                    千分位分割符，如“，”或者“.”
            decimal : str, default ‘.’
                    字符中的小数点 (例如：欧洲数据使用’，‘).
            float_precision : string, default None
                    Specifies which converter the C engine should use for floating-point values. The options are None for the ordinary converter, high for the high-precision converter, and round_trip for the round-trip converter.
            lineterminator : str (length 1), default None
                    行分割符，只在C解析器下使用。
            quotechar : str (length 1), optional
                    引号，用作标识开始和解释的字符，引号内的分割符将被忽略。
            quoting : int or csv.QUOTE_* instance, default 0
                    控制csv中的引号常量。可选 QUOTE_MINIMAL (0), QUOTE_ALL (1), QUOTE_NONNUMERIC (2) or QUOTE_NONE (3)
            doublequote : boolean, default True
                    双引号，当单引号已经被定义，并且quoting 参数不是QUOTE_NONE的时候，使用双引号表示引号内的元素作为一个元素使用。
            escapechar : str (length 1), default None
                    当quoting 为QUOTE_NONE时，指定一个字符使的不受分隔符限值。
            comment : str, default None
                    标识着多余的行不被解析。如果该字符出现在行首，这一行将被全部忽略。这个参数只能是一个字符，空行（就像skip_blank_lines=True）注释行被header和skiprows忽略一样。例如如果指定comment=’#’ 解析‘#empty\na,b,c\n1,2,3’ 以header=0 那么返回结果将是以’a,b,c’作为header。
            encoding : str, default None
                    指定字符集类型，通常指定为’utf-8’. List of Python standard encodings
            dialect : str or csv.Dialect instance, default None
                    如果没有指定特定的语言，如果sep大于一个字符则忽略。具体查看csv.Dialect 文档
            tupleize_cols : boolean, default False
                    Leave a list of tuples on columns as is (default is to convert to a Multi Index on the columns)
            error_bad_lines : boolean, default True
                    如果一行包含太多的列，那么默认不会返回DataFrame ，如果设置成false，那么会将改行剔除（只能在C解析器下使用）。
            warn_bad_lines : boolean, default True
                    如果error_bad_lines =False，并且warn_bad_lines =True 那么所有的“bad lines”将会被输出（只能在C解析器下使用）。
            low_memory : boolean, default True
                    分块加载到内存，再低内存消耗中解析。但是可能出现类型混淆。确保类型不被混淆需要设置为False。或者使用dtype 参数指定类型。注意使用chunksize 或者iterator 参数分块读入会将整个文件读入到一个Dataframe，而忽略类型（只能在C解析器中有效）
            buffer_lines : int, default None
                    不推荐使用，这个参数将会在未来版本移除，因为他的值在解析器中不推荐使用
            compact_ints : boolean, default False
                    不推荐使用，这个参数将会在未来版本移除
                    如果设置compact_ints=True ，那么任何有整数类型构成的列将被按照最小的整数类型存储，是否有符号将取决于use_unsigned 参数
            use_unsigned : boolean, default False
                    不推荐使用：这个参数将会在未来版本移除
                    如果整数列被压缩(i.e. compact_ints=True)，指定被压缩的列是有符号还是无符号的。
            memory_map : boolean, default False
                    如果使用的文件在内存内，那么直接map文件使用。使用这种方式可以避免文件再次进行IO操作。


    to_csv方法定义：
        DataFrame.to_csv(path_or_buf=None, sep=', ', na_rep='', float_format=None, columns=None,
                    header=True, index=True, index_label=None, mode='w', encoding=None, compression=None,
                    quoting=None, quotechar='"', line_terminator='\n', chunksize=None, tupleize_cols=None,
                    date_format=None, doublequote=True, escapechar=None, decimal='.')

        参数详解：
            path_or_buf=None： string or file handle, default None
                    File path or object, if None is provided the result is returned as a string.
                    字符串或文件句柄，默认无文件
                    路径或对象，如果没有提供，结果将返回为字符串。
            sep : character, default ‘,’
                    Field delimiter for the output file.
                    默认字符 ‘ ，’
                    输出文件的字段分隔符。
            na_rep : string, default ‘’
                    Missing data representation
                    字符串，默认为 ‘’
                    浮点数格式字符串
            float_format : string, default None
                    Format string for floating point numbers
                    字符串，默认为 None
                    浮点数格式字符串
            columns : sequence, optional Columns to write
                    顺序，可选列写入
            header : boolean or list of string, default True
                    Write out the column names. If a list of strings is given it is assumed to be aliases for the column names
                    字符串或布尔列表，默认为true
                    写出列名。如果给定字符串列表，则假定为列名的别名。
            index : boolean, default True
                    Write row names (index)
                    布尔值，默认为Ture
                    写入行名称（索引）
            index_label : string or sequence, or False, default None
                    Column label for index column(s) if desired. If None is given, and header and index are True, then the index names are used. A sequence should be given if the DataFrame uses MultiIndex. If False do not print fields for index names. Use index_label=False for easier importing in R
                    字符串或序列，或False,默认为None
                    如果需要，可以使用索引列的列标签。如果没有给出，且标题和索引为True，则使用索引名称。如果数据文件使用多索引，则应该使用这个序列。如果值为False，不打印索引字段。在R中使用index_label=False 更容易导入索引.
            mode : str
                    模式：值为‘str’，字符串
                    Python写模式，默认“w”
            encoding : string, optional
                    编码：字符串，可选
                    表示在输出文件中使用的编码的字符串，Python 2上默认为“ASCII”和Python 3上默认为“UTF-8”。
            compression : string, optional
                    字符串，可选项
                    表示在输出文件中使用的压缩的字符串，允许值为“gzip”、“bz2”、“xz”，仅在第一个参数是文件名时使用。
            line_terminator : string, default ‘\n’
                    字符串，默认为 ‘\n’
                    在输出文件中使用的换行字符或字符序列
            quoting : optional constant from csv module
                    CSV模块的可选常量
                    默认值为to_csv.QUOTE_MINIMAL。如果设置了浮点格式，那么浮点将转换为字符串，因此csv.QUOTE_NONNUMERIC会将它们视为非数值的。
            quotechar : string (length 1), default ‘”’
                    字符串（长度1），默认“”
                    用于引用字段的字符
            doublequote : boolean, default True
                    布尔，默认为Ture
                    控制一个字段内的quotechar
            escapechar : string (length 1), default None
                    字符串（长度为1），默认为None
                    在适当的时候用来转义sep和quotechar的字符
            chunksize : int or None
                    int或None
                    一次写入行
            tupleize_cols : boolean, default False
                    布尔值 ，默认为False
                    从版本0.21.0中删除：此参数将被删除，并且总是将多索引的每行写入CSV文件中的单独行
                    （如果值为false）将多索引列作为元组列表（如果TRUE）或以新的、扩展的格式写入，其中每个多索引列是CSV中的一行。
            date_format : string, default None
                    字符串，默认为None
                    字符串对象转换为日期时间对象
            decimal: string, default ‘.’
                    字符串，默认’。’
                    字符识别为小数点分隔符。例如。欧洲数据使用 ​​’，’

"""

import os
import numpy as np
import pandas as pd


def f1():
    """
        read_csv()
        S.No,Name,Age,City,Salary
        S.No,Name,年龄,城市,Salary
    """
    df = pd.read_csv("a.csv")
    print(df)
    print('='*64)

    #自定义索引
    df = pd.read_csv('a.csv', index_col=['S.No'])
    print(df)
    print('='*64)

    df = pd.read_csv('a.csv', index_col=['City'])
    print(df)
    print('='*64)

    # 转换器 dtype的列可以作为字典传递，转换数据类型
    print(df.dtypes)
    df = pd.read_csv('a.csv', dtype={'Salary':np.float64})
    print(df.dtypes)
    print(df)
    print('='*64)

    #指定标题名称 使用names参数指定标题的名称
    df = pd.read_csv('a.csv', names=['a', 'b', 'c','d','e'])
    print(df)
    print('='*64)

    # 指定标题名称，使用names参数指定标题的名称，header参数删除原标题
    df = pd.read_csv('a.csv', names=['a', 'b', 'c','d','e'], header=0)
    print(df)
    print('='*64)

    # skiprows跳过指定的行数，
    df = pd.read_csv('a.csv')
    print(df)
    print('='*64)
    df = pd.read_csv('a.csv', skiprows=2)   # 跳过开始两行
    print(df)
    print('='*64)
    df = pd.read_csv('a.csv', skiprows=1)   #跳过开始1行
    print(df)
    df = pd.read_csv('a.csv', skiprows=0)
    print(df)
    print('='*64)




def f2():
    """
        to_csv()
    """
    df = pd.read_csv("a.csv")
    print(df.info())
    dt = df.filter(regex="Name|City")
    to_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "to_csv.csv")

    # dt.to_csv(to_file,columns=['Name']) #保存索引列和Name列

    #dt.to_csv(to_file, header=0) # 不保存列名

    #dt.to_csv(to_file, index=0) #不保存行索引


    ids = [1,3,5,7,9]
    values = [1.11,3.33,5.55,7.77,9.99]
    dt = pd.DataFrame({"ids":ids,"values":values})
    dt.to_csv(to_file, index=False)





if __name__ == '__main__':
    #f1()
    f2()
