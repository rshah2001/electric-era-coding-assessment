# Station Uptime Calculator

## What it does
I built this program to calculate how often charging stations are actually available for use. It processes logs of charger availability and figures out what percentage of time each station had at least one working charger.

## Setup
Pretty simple to get running:
- Make sure you have Python 3.7 or newer
- No extra packages needed - just standard Python libraries

## Running it
1. Grab the code
2. Make it executable with:
```bash
chmod +x station_uptime.py
```
3. Run it:
```bash
python station_uptime.py your_input_file.txt
```

## How I built it

### Key Data Structures
I used two main data structures to keep things fast and efficient:
- A dictionary mapping stations to their chargers (using sets for quick lookups)
- Another dictionary linking chargers to their availability reports

### Performance
The algorithm runs in O(N log N) time because we need to sort the timeline events. Memory usage is O(N) since we need to store all the reports - no way around that really.

### Error Cases I Handle
I tried to catch all the ways things could go wrong:
- Bad file formats
- Missing data
- Time ranges that don't make sense
- Wrong command line usage
- File reading issues
- Invalid true/false values

### Edge Cases
I spent a lot of time thinking about edge cases:
- What if the file is empty?
- What about stations with no chargers?
- How do we handle overlapping up/down times?
- What if there are gaps in the reports?
- Multiple chargers at one station?

## Design Decisions

Some key decisions I made while building this:

1. **Overlapping Time Periods**  
When multiple chargers are running at the same time, I count the station as "up" if ANY charger is working. This makes sense from a user's perspective - they just need one working charger.

2. **Gaps in Reports**  
If there's a time period where we don't have any reports, I count that as downtime. Better to be conservative than overstate availability.

3. **Zero Duration Periods**  
If a station has no reports or only zero-duration reports, it gets 0% uptime. Can't claim uptime without data.

## Performance & Scaling

I focused on making this efficient for larger datasets:

1. **Memory Usage**
- Used generators where I could
- Avoided copying data unnecessarily
- Processed data in streams when possible

2. **Processing Speed**
- Used fast lookups with sets and dictionaries
- Minimized sorting operations
- Smart handling of overlapping times

3. **Future Improvements**  
If this needs to handle even bigger datasets, we could:
- Add batch processing
- Split work across multiple cores
- Store historical data in a database

## Code Quality
I tried to keep the code clean and maintainable:
- Followed Python style guides
- Added clear comments
- Used type hints
- Kept the code modular and easy to change