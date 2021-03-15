# Welcome to the Split CLI 👋

The Split CLI is a Command Line Interface built to simplify onboarding, and make it easy to manage your entire feature flag lifecycle. The changes and updates you make to your splits through the CLI will be reflected immediately in the Split UI.

---
Throughout the CLI, to select an option, press the Enter/Return button on your keyboard unless otherwise noted.
---

# 🏠 [Split Homepage](www.split.io)
# 📚 [Split Docs](https://help.split.io/hc/en-us)

## Getting Started

**Note:** Python >=3.6 is required to use the CLI

```sh
pip install splitcli
splitcli
``` 

## New Split Users

Upon running `splitcli`, the CLI will ask you if you have an existing account. Users who are new to Split should select the first option `No, I need to create an account` to create an account. You will be prompted to enter your first name, last name, email address, and phone number. You will then recieve a 6 digit one time password to authenticate. 

## Existing Split Users

If you have a Split account already, select `Yes, take me to sign in` from the initial prompt. You will then enter your email address, followed by your Admin API Key, which can be found in the Admin Settings of your Split profile. For more information on finding your Admin API Key, follow the directions [here](https://www.youtube.com/watch?v=80Bz2ZcZUrs).

# Main Menu

## Manage Splits

A split is another name for a feature flag, which allows you to separate code deployment from feature release. When you select `Manage Splits` from the Main Menu, you will see a list of the splits that are already in your organization, as well as the option to create a new split. 

To create a new split, select `Create a new split` from the menu. You will then be prompted to enter a name for your split, as well as a description. Next, you will choose whether you want a simple rollout, which will give you the ability to turn a feature on or off in any environment, or a custom rollout, where you can have a custom set of treatments.

You will then choose which environment you wish to manage your split in. 

### Show Full Definition JSON

Selecting this option will output the full JSON configuration of your split into your terminal. 

### Target Keys

Selecting this option will allow you to target users into your feature flag. You will select which treatment you are targeting, then add the users.

### Target Segments

Selecting this option will allow you to target a segmented user goup to your feature flag. First select which treatment you are targeting, then select the segments you wish to target by pressing the space bar. 

### Ramp Split

Ramp split allows you to ramp up your split to a specific percentage of users. After selecting this option, you will be prompted to enter percentage of the userbase you wish to be in the ON treatment. 

### Kill Split

Killing a split turns the feature off in the environment you select. To kill a split, navigate to the split, and select `Kill` from the menu.

### Restore Split

Restoring a split turns the split back on after it was killed. Your previous configurations for the Split will still be in place. To restore your split after it has been killed, select `Restore` from the menu.

### Delete Definition

Deleting a split's definition will remove all targeting rules from the split. To delete a split's definition, select `Delete definition` from the menu.

### Delete Split

Once your Split has met its [definition of done](https://www.split.io/blog/feature-flag-done-definition/), it can be deleted. To delete a split, select `Delete split` from the menu. This will delete the split in all environments.

## Manage Segments

Segments are groups of users that you can use to target in your feature flags. When you select `Manage Segments` from the Main Menu, you will see a list of the segments that are already in your organization, as well as the option to create a new segment.

To create a new segment, select `Create a new segment` from the menu. You will then be prompted to enter a name, and description for that segmented user group. Once that segment is created, you will see it listed in the `Manage Segments` menu. Select the segment you created, and choose which environment you wish to manage it in. Here is where we will soon be adding key management capabilities, stay tuned!

To delete a segment, navigate into the segment you wish to delete, and select `Delete segment`.

## Log Out

Selecting Log Out will log you out of the CLI.

## Exit

Selecting Exit will exit out of the CLI.


# Authors

👤 **Talia Nassi**

* Twitter: [@talia_nassi](https://twitter.com/talia_nassi)
* Github: [@talianassi921](https://github.com/talianassi921)

👤 **Henry Jewkes**

* Twitter: [@HenryJewkes](https://twitter.com/HenryJewkes)
* Github: [@HJewkes](https://github.com/HJewkes)

👤 **Micah Silverman**

* Twitter: [@afitnerd](https://twitter.com/afitnerd)
* Github: [@dogeared](https://github.com/dogeared)


## Show your support

Give a ⭐️ if this project helped you!
