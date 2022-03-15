import pandas as pd
import src.utils as utils
import src.data_process as dp
from src.parser import parser


def main(input_file: str, output_file: str, fancy_header: bool):
    """
    Main function of the script.
    Parameters:

        - input_file: string. Indicates the path of the input file

        - output_file: string. Indicates the path of the output file

        - fancy_header: boolean.
        If the user want the output file header to be separated by |
    """

    with open(input_file, 'r') as buffer:
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
        df.to_csv(output_file, sep='\t', index=False, na_rep='NA')
    else:
        with open(output_file, 'w') as filepath:
            filepath.write(' | '.join(df.columns))
        df.to_csv(
            output_file, sep='\t',
            index=False, header=False,
            na_rep='NA', mode='a'
        )


if __name__ == '__main__':
    args = vars(parser.parse_args())
    input_str = args.get('inputfile')
    output_str = args.get('outputfile')
    main(input_str, output_str, fancy_header=False)
