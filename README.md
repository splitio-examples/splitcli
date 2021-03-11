<h1 align="center">Welcome to the Split CLI 👋</h1>
<p>
  <a href="https://twitter.com/talia_nassi" target="_blank">
    <img alt="Twitter: talia_nassi" src="https://img.shields.io/twitter/follow/talia_nassi.svg?style=social" />
  </a>
  <a href="https://twitter.com/HenryJewkes" target="_blank">
    <img alt="Twitter: HenryJewkes" src="https://img.shields.io/twitter/follow/HenryJewkes.svg?style=social" />
  </a>
  <a href="https://twitter.com/afitnerd" target="_blank">
    <img alt="Twitter: afitnerd" src="https://img.shields.io/twitter/follow/afitnerd.svg?style=social" />
  </a>
</p>

The Split CLI is a Command Line Interface built to simplify onboarding, and make it easy to manage your entire feature flag lifecycle. 

### 🏠 [Split Homepage](www.split.io)

## Getting Started

1. Clone this repo

2. Run `splitcli`

# New Split Users

Upon running `splitcli`, the CLI will ask you if you have an existing account. Users who are new to Split should select the first option `No, I need to create an account` to create an account. You will be prompted to enter your first name, last name, email address, and phone number. You will then recieve a 6 digit one time password to authenticate. 

# Existing Split Users

If you have a Split account already, select `Yes, take me to sign in` from the initial prompt. You will then enter your email address, followed by your Admin API Key, which can be found in the Admin Settings of your Split profile. For more information on finding your Admin API Key, follow the directions [here](https://www.youtube.com/watch?v=80Bz2ZcZUrs).

## Main Menu

# Manage Splits

A split is another name for a feature flag, which allows you to separate code deployment from feature release. When you select `Manage Splits` from the Main Menu, you will see a list of the splits that are already in your organization, as well as the option to create a new split. 

To create a new split, select `Create a new split` from the menu. You will then be prompted to enter a name for your split, as well as a description. Next, you will choose whether you want a simple rollout, which will give you the ability to turn a feature on or off in any environment, or a custom rollout, where you can have a custom set of treatments.

You will then choose which environment you wish to manage your split in. 

From the `Managing Split in Environment` Menu, you can configure your split. The first option is to show the full JSON definition of your split, which will output the JSON into your terminal. You can also target keys (users) by selecting `Target keys`. You can also target segments of users by selecting `Target segments`

# Manage Segments

Segments are groups of users that you can use to target in your feature flags. When you select `Manage Segments` from the Main Menu, you will see a list of the segments that are already in your organization, as well as the option to create a new segment.

To create a new segment, select `Create a new segment` from the menu. You will then be prompted to enter a name, and description for that segmented user group. Once that segment is created, you will see it listed in the `Manage Segments` menu. Select the segment you created, and choose which environment you wish to manage it in. Here, keys refer to the users in that group. To show the keys for the segment, select `Show keys`. To add keys for the segment, select `Add keys`. To remove keys for the segment, select `Remove keys`. You can also do a bulk upload of users with a CSV file by selecting `Upload CSV`.

To delete a segment, navigate into the segment you wish to delete, and select `Delete segment`.

# Manage Metrics

# Manage Organization

# Log Out

Selecting Log Out will log you out of the CLI.

# Exit

Selecting Exit will exit out of the CLI.


## Authors

👤 **Talia Nassi**

* Twitter: [@talia_nassi](https://twitter.com/talia_nassi)
* Github: [@talianassi921](https://github.com/talianassi921)

👤 **Henry Jewkes**

* Twitter: [@HenryJewkes](https://twitter.com/HenryJewkes)
* Github: [@HJewkes](https://github.com/HJewkes)

👤 **Micah Silverman**

* Twitter: [@afitnerd](https://twitter.com/afitnerd)
* Github: [@dogeared](https://github.com/dogeared)

## Build locally

Split CLI requires Python 3.6 at minimum.

## Coming soon to PyPi!

## Show your support

Give a ⭐️ if this project helped you!
