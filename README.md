# Alibaba Ticket Availability Checker

A Selenium-based automation tool that checks ticket availability and pricing pages for flights, trains, and buses on Alibaba.ir (a major Iranian travel booking platform), built as a practical web scraping exercise for handling dynamic, JavaScript-rendered websites.

## Overview

Given an origin, destination, travel date, and vehicle type (flight, train, or bus), the script automates the full search flow on Alibaba.ir: navigating to the correct travel tab, filling in origin and destination fields, navigating the calendar widget to select the target date, and triggering the search. It then reports whether matching tickets are available and returns the resulting search results URL.

## How It Works

1. **Vehicle selection** — navigates to the correct tab (flight, train, or bus) based on the requested vehicle type, since each tab has a different page structure and input selectors
2. **Origin & destination input** — types the city name into the relevant autocomplete fields and confirms the selection
3. **Date navigation** — programmatically advances the calendar widget month by month until the target month is found, then selects the target day
4. **Search execution** — clicks the search button (selector differs between flights and other vehicle types) and waits for results to load
5. **Result extraction** — checks whether any ticket results are rendered on the page and returns the availability status along with the final URL as JSON

## Tech Stack

- **Selenium** (WebDriver, Explicit Waits, `expected_conditions`) for browser automation
- **XPath & CSS Selectors** for locating dynamic, JavaScript-rendered elements
- Handles asynchronous page loads, autocomplete dropdowns, and a multi-step calendar UI

## Notes

This was built as a practical exercise in scraping dynamic websites that rely heavily on client-side rendering and interactive widgets (autocomplete fields, custom date pickers), going beyond static HTML parsing into full browser automation and explicit wait strategies.
