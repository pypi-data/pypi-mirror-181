import logging
from pathlib import Path

import click
from click_option_group import RequiredMutuallyExclusiveOptionGroup, optgroup

from court_scraper import utils
from court_scraper.configs import Configs
from court_scraper.datastore import Datastore
from court_scraper.sites_meta import SitesMeta


@click.group()
def cli():
    pass


@cli.command(help="Search and scrape case info from county court site.")
@click.option(
    "-p",
    "--place-id",
    required=True,
    help="A unique place ID made up of the state and county (e.g. ga_dekalb)",
)
@optgroup.group(
    "Case number sources",
    cls=RequiredMutuallyExclusiveOptionGroup,
    help="Case numbers must be supplied on the command line or via text file.",
)
@optgroup.option("-c", "--case-number", help="A case number to search.")
@optgroup.option(
    "-f",
    "--case-numbers-file",
    type=click.File("r"),
    help="Text file containing one or more case numbers.",
)
@click.option(
    "--with-browser",
    is_flag=True,
    help="Open graphical browser during Selenium-based scrapes. By default, runs headless.",
)
def search(place_id, case_number, case_numbers_file, with_browser):
    """Search court site."""
    # Config and logging setup
    configs = Configs()
    cache_dir = Path(configs.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    log_file = str(cache_dir.joinpath("logfile.txt"))
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)-12s - %(message)s",
        datefmt="%m-%d %H:%M",
        filename=log_file,
        filemode="a",
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)
    logger = logging.getLogger(__name__)
    # Get Runner and execute the search
    RunnerKlass = utils.get_runner(place_id)
    runner = RunnerKlass(configs.cache_dir, configs.config_file_path, place_id)
    if case_number:
        case_numbers = [case_number]
    else:
        case_numbers = [t.strip() for t in case_numbers_file]
    kwargs = {
        "case_numbers": case_numbers,
        "headless": not with_browser,
    }
    # TODO: Restore catch-all try/except
    results = runner.search(**kwargs)
    runner.cache_detail_pages(results)
    dstore = Datastore(configs.db_path)
    logger.info(f"Adding {len(results)} results to {configs.db_path}")
    to_db = []
    for result in results:
        # Place ID is required Case db table
        result.place_id = place_id
        to_db.append(result.standard_data)
    dstore.upsert(to_db)


@cli.command(help="Get info about available scrapers")
def info():
    """Print inforomation about the available scrapers."""
    msg = "\nAvailable scrapers:\n\n"
    meta = SitesMeta()
    for state, county in meta.data.keys():
        place_id = f"{state}_{county.replace(' ', '_')}"
        msg += f" * {state.upper()} - {county.title()} ({place_id})\n"
    end_note = (
        "\nNOTE: Scraper IDs (in parentheses) should be "
        + "used with the search command's --place-id argument."
    )
    msg += end_note
    click.echo(msg)


if __name__ == "__main__":
    cli()
