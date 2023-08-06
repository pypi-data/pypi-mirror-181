import sys
sys.path.append('../')
import lightpandas as lpd


def main():
    df = lpd.read_csv(filepath_or_buf='test_with_index.csv', index_col=0)
    df.to_csv('test_tmp.csv', index=False)


if __name__ == '__main__':
    main()
