Feature: Get users based on task completion
  Of all users,
  I want users that belong to FanCode city,
  I want users who have completed more than 50% of their tasks.

  Scenario: Get users of city FanCode with more than half of their todos task completed
    Given user has todos tasks
    And user belongs to the city "FanCode"
    Then user completed task are more than "half"