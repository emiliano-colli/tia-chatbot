## ADDED Requirements

### Requirement: Composer chrome stays compact on a narrow viewport
On a typical phone viewport (~360px wide) the chat page footer MUST hug its content. The farewell hint, new-conversation control and message composer MUST appear stacked with only normal control spacing between them. MUST NOT leave a large empty block (on the order of several rem of unused flex height) between the farewell hint and the message input.

#### Scenario: No large gap between hint and input
- **WHEN** the chat page is viewed at approximately 360px width
- **THEN** the vertical space between the farewell hint text and the message input is limited to the stacked “Nueva consulta” control and normal padding/gaps, not an empty flex-grown region
