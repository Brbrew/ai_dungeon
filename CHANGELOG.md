# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2025-04-21

### Added
- Implemented TAKE action to pick up items from rooms
- Implemented DROP action to place items from inventory into rooms
- Enhanced INVENTORY action to display item names and types
- Added alias attribute to Item class for improved command parsing
- Added room_item_location parameter to Room class
- Added theme icons to the Theme class for enhanced map visualization
- Updated SVG map generation to use theme-specific icons instead of circles
- Enhanced map UI with hover effects and visited/unvisited room styling
- Improved map display with responsive sizing and better positioning
- Added icons to the UI for Map, Inventory, etc.

### Fixed
- Fixed TypeError in DROP action when accessing player inventory items
- Corrected item handling in parse_command method to properly distinguish between room items and inventory items

## [0.0.1] - 2025-04-20

### Added
- Initial release of the Dungeon project
- Basic dungeon generation and navigation
- Character system with inventory management
- Room-based exploration with connections
- SVG map generation with dynamic sizing
- Command parsing for player interactions
- AI-powered room descriptions

### Changed
- Improved room placement algorithm to prevent overlaps
- Enhanced SVG map generation for better visibility

### Fixed
- Fixed issue with room connections not being displayed correctly
- Resolved problem with SVG being cut off in the HTML container 