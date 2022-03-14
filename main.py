import pandas as pd
import src.utils as utils
import src.data_process as dp


def main(output: str, fancy_header: bool):
    """
    Main function of the script.
    Parameters:

        - output: string. Indicates the path of the output file

        - fancy_header: boolean.
        If the user want the output file header to be separated by |
    """
    with open('pretrade_current.txt', 'r') as buffer:
        msg_type, _ = utils.get_msgType_dict(buffer)

    df8 = utils.generate_DataFrame_by_type_id('8', input_table=msg_type)
    df12 = utils.generate_DataFrame_by_type_id('12', input_table=msg_type)

    df8 = dp.clean_type_8(df8)
    df12 = dp.aggregate_type_12(df12)

    df = pd.concat(
        [df8, df12],
        join='inner',
        axis=1
        )

    if not fancy_header:
        df.to_csv(output, sep='\t', index=False, na_rep='NA')
    else:
        with open(output, 'w') as filepath:
            filepath.write(' | '.join(df.columns))
        df.to_csv(
            output, sep='\t',
            index=False, header=False,
            na_rep='NA', mode='a'
        )


if __name__ == '__main__':
    main('aggregate_output.tsv', fancy_header=False)
