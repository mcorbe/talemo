# End-to-End Tests

This directory contains end-to-end (E2E) tests for the Talemo platform. E2E tests validate complete user journeys from start to finish, simulating real user interactions with the application.

## Overview

End-to-end tests are at the top of the testing pyramid. They test the entire application stack, from the user interface down to the database, ensuring that all components work together correctly to deliver the expected user experience.

## Directory Structure

The E2E tests are organized by user journey or feature:

```
e2e/
├── cypress/              # Cypress test configuration and support files
│   ├── fixtures/         # Test data
│   ├── integration/      # Test specs
│   │   ├── stories/      # Story-related tests
│   │   ├── agents/       # Agent-related tests
│   │   └── assets/       # Asset-related tests
│   ├── plugins/          # Cypress plugins
│   └── support/          # Support files and commands
├── cypress.json          # Cypress configuration
└── README.md             # This file
```

## Test Framework

The E2E tests use [Cypress](https://www.cypress.io/), a JavaScript-based end-to-end testing framework that runs in the browser. Cypress provides a rich set of features for writing and debugging tests, including:

- Time travel debugging
- Real-time reloads
- Automatic waiting
- Network traffic control
- Screenshots and videos

## Writing E2E Tests

### Test File Naming

E2E test files should follow the naming convention:

```
<feature>_spec.js
```

For example:
- `story_creation_spec.js` - Tests for the story creation flow
- `story_playback_spec.js` - Tests for the story playback flow
- `agent_playground_spec.js` - Tests for the agent playground

### Test Structure

Cypress tests are organized using Mocha's `describe` and `it` functions:

```javascript
// cypress/integration/stories/story_creation_spec.js
describe('Story Creation', () => {
  beforeEach(() => {
    // Set up test data and authenticate
    cy.login('testuser', 'password');
    cy.visit('/stories/create');
  });

  it('should create a new story', () => {
    // Fill out the story creation form
    cy.get('#prompt-input').type('A story about a curious cat');
    cy.get('#age-range-select').select('4-8');
    
    // Submit the form
    cy.get('button[type="submit"]').click();
    
    // Wait for the story to be generated
    cy.get('.status-indicator', { timeout: 30000 }).should('contain', 'Complete');
    
    // Verify the story was created
    cy.get('.story-title').should('be.visible');
    cy.get('.story-content').should('be.visible');
    
    // Verify navigation to the story detail page
    cy.url().should('include', '/stories/');
  });

  it('should show an error message for invalid input', () => {
    // Submit the form without filling it out
    cy.get('button[type="submit"]').click();
    
    // Verify error messages
    cy.get('.error-message').should('be.visible');
    cy.get('.error-message').should('contain', 'Please enter a story prompt');
  });
});
```

### Custom Commands

Create custom Cypress commands for common operations:

```javascript
// cypress/support/commands.js
Cypress.Commands.add('login', (username, password) => {
  cy.visit('/accounts/login/');
  cy.get('#id_username').type(username);
  cy.get('#id_password').type(password);
  cy.get('button[type="submit"]').click();
  cy.url().should('not.include', '/accounts/login/');
});

Cypress.Commands.add('createStory', (prompt, ageRange) => {
  cy.visit('/stories/create');
  cy.get('#prompt-input').type(prompt);
  cy.get('#age-range-select').select(ageRange);
  cy.get('button[type="submit"]').click();
  cy.get('.status-indicator', { timeout: 30000 }).should('contain', 'Complete');
});
```

## Testing User Journeys

Focus on testing complete user journeys that represent real user interactions:

1. **Story Creation Journey**:
   - User logs in
   - Navigates to story creation page
   - Enters a prompt and selects age range
   - Submits the form
   - Waits for the story to be generated
   - Reviews and publishes the story

2. **Story Playback Journey**:
   - User logs in
   - Browses available stories
   - Selects a story
   - Plays the audio
   - Navigates through illustrations
   - Pauses and resumes playback

3. **Agent Playground Journey**:
   - User logs in
   - Navigates to agent playground
   - Selects an agent type
   - Enters input parameters
   - Submits the request
   - Views the agent output

## Running E2E Tests

### Running Tests Locally

To run E2E tests locally:

```bash
# Open Cypress test runner
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py cypress open

# Run tests headlessly
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py cypress run
```

### Running Specific Tests

To run a specific test file:

```bash
docker-compose -f docker/docker-compose.dev.yml exec web python manage.py cypress run --spec "cypress/integration/stories/story_creation_spec.js"
```

## Best Practices

- **Focus on user journeys**: Test complete user flows rather than individual features.
- **Use realistic test data**: Create test data that resembles real-world scenarios.
- **Keep tests independent**: Each test should be able to run independently of others.
- **Handle asynchronous operations**: Use Cypress's automatic waiting and explicit waits when needed.
- **Use custom commands**: Create custom commands for common operations to keep tests DRY.
- **Test for accessibility**: Include tests for accessibility compliance.
- **Test on multiple viewports**: Test on different screen sizes to ensure responsive design.

## Related Documentation

- [Cypress Documentation](https://docs.cypress.io/)
- [Cypress Best Practices](https://docs.cypress.io/guides/references/best-practices)
- [Django Cypress Integration](https://github.com/cypress-io/cypress-documentation/blob/master/source/guides/guides/django.md)