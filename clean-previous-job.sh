#/bin/bash
rm -f mycrawler-all.jsonl
rm -f logs/defacementcrawler.log
rm -rf jobs/mycrawler/*
find files_downloaded/ -type f -name "*" -exec rm {} \;
#rm -f files_downloaded/*
