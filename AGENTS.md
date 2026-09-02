# AGENTS.md - Development Guidelines & Constraints

## Project Overview

**Project:** Number Adventure - Educational Learning App
**Purpose:** Teach children numbers 1-10, addition, and subtraction with audio and animations
**Live URL:** https://nanapaknanapak-huemirit.github.io/learn-numbers-kids/

---

## Mandatory Constraints

### 1. Modular Code Architecture

**RULE: All code MUST be modular and follow separation of concerns.**

- **HTML** → Structure only, no inline styles or scripts
- **CSS** → Styling only, use CSS variables for theming
- **JavaScript** → Logic only, organize into clear modules/sections

**Requirements:**
- Each function should do ONE thing well
- Break large functions into smaller, testable units
- Use configuration objects instead of scattered constants
- Group related functionality together with clear comments

**Example:**
```javascript
// BAD - Everything mixed together
function handleClick() {
    document.getElementById('score').textContent = score;
    const audio = new Audio('audio/en/one.mp3');
    audio.play();
}

// GOOD - Separated concerns
function updateScoreDisplay() {
    document.getElementById('score').textContent = score;
}

function playAudio(filename) {
    return new Promise((resolve) => {
        const audio = new Audio(`${AUDIO_BASE_PATH}/${currentLang}/${filename}.mp3`);
        audio.onended = resolve;
        audio.play().catch(resolve);
    });
}
```

---

### 2. No Hardcoded Values

**RULE: NEVER hardcode values that could change or vary.**

**Prohibited:**
```javascript
// BAD - Hardcoded paths
const audio = new Audio('audio/en/one.mp3');

// BAD - Hardcoded strings
showMessage("Great job!");

// BAD - Hardcoded numbers
let answer = 5 + 3;
```

**Required:**
```javascript
// GOOD - Configuration-based
const AUDIO_BASE_PATH = 'audio';
const audio = new Audio(`${AUDIO_BASE_PATH}/${currentLang}/${filename}.mp3`);

// GOOD - Language-aware
const lang = languages[currentLang];
showMessage(lang.messages.correct);

// GOOD - Dynamic calculation
let answer = num1 + num2;
```

**Configuration Objects:**
- All paths → Use constants
- All UI text → Use language configuration
- All magic numbers → Use named constants
- All colors → Use CSS variables

---

### 3. Anti-Tactical-Tornado Policy

**RULE: No "tactical tornado" refactoring or quick hacks.**

A "tactical tornado" is when someone:
- Makes quick, messy changes "just to make it work"
- Adds technical debt intentionally
- Skips proper implementation for speed
- Says "we'll fix it later" (but never does)

**Prevention Strategies:**

1. **Plan Before Coding**
   - Understand the requirement fully
   - Design the solution mentally
   - Consider edge cases

2. **Code for Clarity**
   - Write code that explains itself
   - Use meaningful variable names
   - Add comments for complex logic only

3. **Test As You Go**
   - Verify each change works
   - Don't accumulate broken code
   - Fix issues immediately

4. **Refactor Properly**
   - If code needs changing, do it right
   - Don't patch over problems
   - Take time to do it properly

**Red Flags to Avoid:**
- `// TODO: fix this later`
- `// HACK: temporary solution`
- `// WORKAROUND:`
- Comments explaining why code is messy
- Deeply nested if/else statements
- Functions doing multiple things

---

### 4. Dead Code Cleanup

**RULE: Remove ALL dead elements immediately after they're no longer needed.**

**Dead Elements Include:**
- Unused variables
- Commented-out code
- Unreachable code blocks
- Unused functions
- Unused CSS classes
- Unused imports
- Empty event handlers
- Placeholder content

**Detection:**
```bash
# Before committing, check for:
# 1. Unused variables (use linter)
# 2. Commented-out code (grep for //)
# 3. Unused CSS classes (manual review)
# 4. Dead functions (manual review)
```

**Cleanup Process:**
1. Identify dead code
2. Verify it's truly unused (search entire codebase)
3. Remove completely
4. Test to ensure nothing broke
5. Commit clean code

**Never Leave:**
- Old debug `console.log` statements
- Commented-out features
- Unused CSS classes
- Temporary workarounds
- Dead function stubs

---

### 5. Maintainable Code Standards

**RULE: Write code that others can understand and maintain.**

**Code Style:**
- Use consistent indentation (2 or 4 spaces)
- Follow language conventions (camelCase for JS, kebab-case for CSS)
- Keep lines under 100 characters when possible
- Use meaningful, descriptive names

**Documentation:**
- Add JSDoc comments for public functions
- Explain complex algorithms
- Document configuration options
- Keep README up to date

**Error Handling:**
- Always handle potential errors
- Provide meaningful error messages
- Don't silently fail
- Use try/catch for async operations

**Example:**
```javascript
/**
 * Plays an audio file for the current language
 * @param {string} filename - Name of the audio file (without .mp3)
 * @returns {Promise<void>} Resolves when audio finishes or fails
 */
async function playAudio(filename) {
    try {
        if (currentAudio) {
            currentAudio.pause();
            currentAudio.currentTime = 0;
        }

        const audio = new Audio(`${AUDIO_BASE_PATH}/${currentLang}/${filename}.mp3`);
        currentAudio = audio;
        
        return new Promise((resolve) => {
            audio.onended = () => {
                currentAudio = null;
                resolve();
            };
            
            audio.onerror = (e) => {
                console.warn(`Audio playback failed: ${currentLang}/${filename}`, e);
                currentAudio = null;
                resolve();
            };
            
            audio.play().catch((e) => {
                console.warn(`Audio play rejected: ${currentLang}/${filename}`, e);
                currentAudio = null;
                resolve();
            });
        });
    } catch (error) {
        console.error(`Unexpected error in playAudio: ${filename}`, error);
        currentAudio = null;
    }
}
```

---

## Project-Specific Guidelines

### Audio System

**Current Architecture:**
```
audio/
├── en/          # English
├── es/          # Spanish
├── de/          # German
├── fr/          # French
├── nl/          # Dutch
├── pt/          # Portuguese
├── it/          # Italian
├── ja/          # Japanese
└── zh/          # Chinese
```

**Adding New Languages:**
1. Create language folder: `audio/{lang_code}/`
2. Generate audio files using Edge TTS
3. Add language configuration to `languages` object in JS
4. Add language button to HTML
5. Update UI translations
6. Test all audio paths work

**Audio File Naming:**
- Numbers: `{word}.mp3` (e.g., `one.mp3`, `uno.mp3`)
- Operations: `{word}.mp3` (e.g., `plus.mp3`, `más.mp3`)
- Encouragement: `{phrase-with-dashes}.mp3` (e.g., `great-job.mp3`)
- Equations: `{num1}-{op}-{num2}.mp3` (e.g., `add-1-2.mp3`)

---

### Language Configuration

**Structure:**
```javascript
const languages = {
    langCode: {
        name: 'Language Name',
        numbers: { 1: 'word', 2: 'word', ... },
        plus: 'operator',
        minus: 'operator',
        equals: 'operator',
        encouragement: ['phrase-1', 'phrase-2', ...],
        messages: {
            numbers: 'UI text',
            addition: 'UI text',
            // ... other messages
        }
    }
};
```

**Adding New Language:**
1. Research correct number words
2. Research correct math operators
3. Find culturally appropriate encouragement phrases
4. Generate audio files with Edge TTS
5. Test pronunciation with native speaker if possible

---

### UI/UX Guidelines

**Visual Design:**
- Use CSS variables for colors (easy theming)
- Maintain consistent spacing
- Ensure mobile responsiveness
- Use accessible color contrasts

**Animations:**
- Keep animations under 500ms
- Use `transform` and `opacity` for performance
- Provide reduced-motion option if needed
- Don't animate during user input

**Accessibility:**
- Use semantic HTML
- Add ARIA labels where needed
- Ensure keyboard navigation works
- Test with screen readers

---

### Git Workflow

**Commit Messages:**
```
type(scope): description

Examples:
feat(audio): add Japanese language support
fix(numbers): correct star display on mobile
refactor(addition): extract answer validation logic
cleanup: remove unused CSS classes
```

**Branch Strategy:**
- `main` → Production ready
- `develop` → Integration branch
- `feature/*` → New features
- `fix/*` → Bug fixes
- `cleanup/*` → Code cleanup

**Before Committing:**
1. Run any linting/formatting tools
2. Test in multiple browsers
3. Verify mobile responsiveness
4. Check for dead code
5. Ensure no hardcoded values

---

### Performance Guidelines

**Audio:**
- Lazy load audio files
- Cache audio elements
- Stop previous audio before playing new
- Handle network errors gracefully

**Images/Assets:**
- Use appropriate formats (SVG for icons)
- Optimize file sizes
- Lazy load non-critical assets

**JavaScript:**
- Minimize DOM manipulation
- Use event delegation
- Avoid memory leaks (clean up event listeners)
- Throttle/debounce frequent events

---

### Testing Checklist

**Before Release:**
- [ ] All numbers (1-10) speak correctly in all languages
- [ ] Addition mode works with all valid combinations
- [ ] Subtraction mode works with all valid combinations
- [ ] Language switching works seamlessly
- [ ] All encouragement phrases play correctly
- [ ] Mobile responsiveness verified
- [ ] No console errors
- [ ] No dead code remaining
- [ ] All values are configurable
- [ ] Code is properly modular

---

### Common Pitfalls to Avoid

1. **Hardcoded Language Text** → Use language configuration
2. **Mixed Concerns** → Keep HTML, CSS, JS separate
3. **Dead Code** → Remove immediately after use
4. **Magic Numbers** → Use named constants
5. **Nested Callbacks** → Use async/await
6. **Missing Error Handling** → Always handle failures
7. **Inconsistent Naming** → Follow conventions
8. **No Documentation** → Add JSDoc for public APIs
9. **Untested Changes** → Test before committing
10. **Technical Debt** → Fix properly, not temporarily

---

## Quick Reference

**Adding a Feature:**
1. Plan the implementation
2. Write modular code
3. Use configuration objects
4. Handle errors
5. Remove dead code
6. Test thoroughly
7. Document if complex
8. Commit with clear message

**Fixing a Bug:**
1. Understand the root cause
2. Write a test to prevent regression
3. Fix the actual issue (not symptoms)
4. Verify fix works
5. Check for related issues
6. Commit with clear message

**Refactoring:**
1. Understand current behavior
2. Make small, incremental changes
3. Test after each change
4. Don't change behavior during refactor
5. Remove old code completely
6. Commit refactoring separately

---

## Final Reminders

- **Modular** → Small, focused functions
- **Maintainable** → Clear, documented code
- **No Tornadoes** → Do it right, not fast
- **Clean** → Remove dead code immediately
- **Configurable** → No hardcoded values

**Remember:** Code is read more often than it's written. Write for the next developer (which might be you in 6 months).

---

*Last updated: 2026-09-02*
