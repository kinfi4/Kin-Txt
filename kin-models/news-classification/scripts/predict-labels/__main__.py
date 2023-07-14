import click

from .predict import make_predictions


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("file-path")
@click.option("--model-path", "-m", help="Path to model")
@click.option("--tokenizer-path", "-t", help="Path to tokenizer")
@click.option("--label-encoder-path", "-l", help="Path to label encoder")
def predict(file_path: str, model_path: str, tokenizer_path: str, label_encoder_path: str) -> None:
    if not file_path.endswith(".csv"):
        print("File should be .csv file")
        return

    make_predictions(file_path, model_path, tokenizer_path, label_encoder_path)


if __name__ == '__main__':
    cli()
