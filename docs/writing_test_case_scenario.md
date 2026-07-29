---
title: "Writing Test Case Scenario"
author:
  - Joseph Garnier
---

# Writing test case scenario

## Anatomy of a test case

Well-structured test cases follow consistent formats ensuring clarity and completeness. Understanding each component enables writing test cases that others can execute reliably.

### 1. Test Case Identifier

Every test case requires unique identification enabling precise reference in test plans, defect reports, and traceability matrices. Identifiers typically follow patterns like TC001, REGRESSION_LOGIN_001, or MODULE_FEATURE_001, incorporating system, module, or feature context for clarity.

### 2. Test Case Title

Concise, descriptive titles immediately communicate what the test validates. Effective titles use action verbs and specify the exact scenario: "Verify successful user login with valid credentials," "Validate error message for invalid email format," "Confirm order total calculation with multiple discounts." Poor titles like "Login test" or "Test 1" provide insufficient context.

### 3. Test Description

Brief descriptions provide additional context beyond titles, explaining the test's purpose and what aspect of functionality it validates. For example: "This test verifies that users can successfully authenticate using registered email addresses and passwords, gaining access to their account dashboard upon successful login."

### 4. Preconditions

Preconditions specify the system state and data that must exist before test execution begins. "User account exists in database with email test@example.com and password Test123!," "Application is deployed to QA environment," "Test database contains sample product catalog," "User is logged out of the application."

Clearly defined preconditions ensure testers can establish appropriate starting conditions rather than encountering test failures due to improper setup.

### 5. Test Steps

Test steps provide sequential instructions for executing the test. Each step should be specific, actionable, and unambiguous. Rather than "Login to application," write "Navigate to login page at https://app.example.com/login, Enter 'test@example.com' in Email field, Enter 'Test123!' in Password field, Click 'Sign In' button."

Granular steps eliminate ambiguity. When tests fail, specific steps enable identifying exactly where execution diverged from expected behavior.

### 6. Test Data

Specify exact test data required for execution. "Email: test@example.com," "Password: Test123!," "Product SKU: WIDGET-001," "Discount Code: SAVE20." Documenting test data ensures reproducibility and enables maintaining test data separately from test steps for reusability.

### 7. Expected Results

Expected results define correct system behavior after executing each test step or at test completion. "User redirects to dashboard at https://app.example.com/dashboard," "Welcome message displays: 'Welcome back, John Doe'," "Session cookie sets with 24-hour expiration," "Last login timestamp updates in database."

Precise expected results enable objective pass/fail determination rather than subjective judgment about whether behavior seems correct.

### 8. Actual Results

During test execution, testers document actual observed behavior. When actual results match expected results, tests pass. Discrepancies indicate defects requiring investigation and remediation.

### 9. Test Status

Test cases maintain status throughout their lifecycle: Draft (being written), Ready for Review, Approved, Blocked (cannot execute due to dependencies), Pass (executed successfully), Fail (defect identified), Skip (not applicable for current release).

### 10. Priority and Severity

Priority indicates execution order and importance. Critical tests validate fundamental functionality like user authentication or payment processing. High priority tests cover major features. Medium and low priority tests address secondary functionality or edge cases.

Test case priority informs regression testing strategies when time constraints prevent executing complete test suites.

## Template

```markdown
Test Case ID: <Unique identifier>
Test Case Title: <Concise descriptive title>
Test Description: <Brief explanation of purpose>
Module/Feature: <Application area being tested>
Priority: <Critical|High|Medium|Low>
Preconditions: <Required system state and data>

Test Steps:

1. <First specific action>
2. <Second specific action>
3. <Continue for all steps>

Test Data:

- <List all required data inputs>

Expected Results:

- <Specific expected outcome for each critical step>
- <Final expected state after test completion>

Actual Results: <To be completed during execution>
Status: <Pass|Fail|Blocked|Skip>
Notes: <Any additional observations>
```

## Examples

### Login functionality

```markdown
**TC_LOGIN_001 - Verify successful login with valid credentials**

Test Case ID: TC_LOGIN_001
Test Case Title: Verify successful login with valid credentials
Test Description: -
Module/Feature: -
Priority: -
Preconditions: User account exists (email: testuser@example.com, password: Test123!)

Test Steps:

1. Open application login page
2. Enter "testuser@example.com" in email field
3. Enter "Test123!" in password field
4. Click "Sign In" button
‍
Test Data: -

Expected Results:

- User navigates to dashboard page
- Welcome message displays user's name
- Logout button appears in navigation
- Session establishes with 24-hour timeout
‍
Actual Results: -
Status: -
Notes: -
```

```markdown
**TC_LOGIN_002 - Verify error message for invalid password**

Test Case ID: TC_LOGIN_002
Test Case Title: Verify error message for invalid password
Test Description: -
Module/Feature: -
Priority: -
Preconditions: User account exists (email: testuser@example.com)

Test Steps:

1. Open application login page
2. Enter "testuser@example.com" in email field
3. Enter "WrongPassword123" in password field
4. Click "Sign In" button
‍
Test Data: -

Expected Results:

- User remains on login page
- Error message displays: "Invalid email or password"
- Email field retains entered value
- Password field clears
- Login attempt logs for security monitoring
‍
Actual Results: -
Status: -
Notes: -
```

### E-commerce checkout

```markdown
**TC_CHECKOUT_001 - Verify successful order placement**

Test Case ID: TC_CHECKOUT_001
Test Case Title: Verify successful order placement
Test Description: -
Module/Feature: -
Priority: -

Preconditions:

- User is logged in
- Shopping cart contains products totaling $50
- User has saved payment method

Test Steps:

1. Navigate to shopping cart
2. Click "Proceed to Checkout"
3. Verify shipping address displays correctly
4. Select "Standard Shipping" option
5. Review order summary
6. Click "Place Order" button
‍
Test Data: -

Expected Results:

- Order confirmation page displays with order number
- Confirmation email sends to user
- Payment processes successfully
- Inventory decrements for purchased products
- Order appears in user's order history
- Order status shows "Processing"
‍
Actual Results: -
Status: -
Notes: -
```

### Search functionality

```markdown
**TC_SEARCH_001 - Verify search returns relevant results for a valid query**

Test Case ID: TC_SEARCH_001
Test Case Title: Verify search returns relevant results for a valid query
Test Description: -
Module/Feature: -
Priority: -

Preconditions:

- Application is accessible and logged in
- Product catalogue contains at least 20 products including items with the keyword "wireless"

Test Steps:

1. Navigate to the search bar at the top of the page
2. Enter "wireless" in the search field
3. Press Enter or click the search icon
4. Review the results page
‍
Test Data: -

Expected Results:

- Search results page loads within two seconds
- All results displayed contain "wireless" in the product name or description
- Result count displays the correct number of matching products
- No results outside the search term appear on the first page
‍
Actual Results: -
Status: -
Notes: -
```

## Best practices for test case writing

### 1. Write for clarity and simplicity

Test cases should be understandable to anyone on the QA team, not just the author. Use simple, direct language. Avoid jargon unless it is standard terminology everyone understands. Each test case should validate one specific aspect of functionality rather than combining multiple unrelated tests.

### 2. Maintain Independence

Test cases should execute independently without depending on other test cases running first. Each test establishes its own preconditions rather than assuming a previous test left the system in a particular state. This independence enables parallel execution and reordering test sequences without breaks.

### 3. Include Negative Test Cases

Positive test cases verify systems work correctly with valid inputs. Negative test cases verify systems handle invalid inputs gracefully. Comprehensive testing requires both. For every valid input scenario, consider invalid alternatives: wrong data types, missing required fields, values outside acceptable ranges, boundary conditions.

### 4. Keep Test Cases Current

Test cases decay when applications evolve but documentation does not. Establish processes for updating test cases when requirements change, user interfaces are redesigned, or business logic updates. Outdated test cases waste execution time and create false defect reports.

### 5. Use Clear Naming Conventions

Consistent naming enables quick identification of test scope and purpose. Include module names, feature identifiers, and scenario types in test case IDs. "AUTH_LOGIN_VALID_001" immediately indicates authentication module, login feature, valid credentials scenario.

### 6. Document Assumptions

Make implicit assumptions explicit. If a test assumes browser cookies are enabled, document that assumption. If the test requires specific user permissions, state that explicitly. Documented assumptions prevent confusion when tests fail due to unmet preconditions.

## Références

- [How to Write Test Cases in Manual Testing (Templates & Examples)](https://www.virtuosoqa.com/post/write-test-cases-in-manual-testing#test-case-templates-and-examples).
- [6 Test Documentation Templates to Streamline Software Testing](https://scribe.com/library/test-documentation-templates).
