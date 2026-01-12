# CraftLogic: Crochet 
**Version 0.1 — Console Prototype**

CraftLogic: Crochet is an early-stage pattern-planning tool designed to help crocheters calculate blanket dimensions, borders, and estimated yarn requirements without guesswork.

This version is a **Python console prototype**, built to validate logic, user flow, and core calculations before moving toward a graphical or mobile interface.

---

## What CraftLogic Does (v0.1)

- Guides users through blanket planning step-by-step
- Supports preset sizes (baby, throw, twin, queen)
- Allows fully custom dimensions in multiple units
- Handles borders (type, width, inclusion in finished size)
- Calculates body size vs finished size accurately
- Estimates yarn yardage ranges
- Includes a demo “recreate from photo” workflow for granny-square blankets
- Designed with beginner-friendly prompts and error handling

---

## Project Goals

This project was created to:

- Reduce friction and math anxiety in crochet project planning  
- Explore user-centered input validation and navigation logic  
- Serve as a foundation for a future GUI or mobile app  
- Demonstrate clean, readable Python code suitable for a portfolio  

---

## Design Decisions

- **Console-first approach**: Focused on correctness and flow before UI
- **Explicit back (`b`) and quit (`q`) navigation**: Designed for real user mistakes
- **Readable logic over clever shortcuts**: Prioritized clarity and maintainability
- **Versioned workflow**: v0.1 is intentionally limited and stable

---

## Known Limitations (v0.1)

- Console-based (no GUI yet)
- Yardage estimates are approximate (v1 math model)
- “Recreate from photo” is a logic demo, not actual image processing
- Back navigation returns to earlier steps rather than exact previous state

These are intentional tradeoffs for an early prototype.

---

## Planned Future Work

- Graphical or mobile interface
- More accurate yarn calculations
- Stitch pattern selection
- Saved projects
- Image-based pattern analysis
- Accessibility improvements

---

## How to Run

1. Ensure Python 3.10+ is installed
2. Clone the repository
3. Run:

```bash
