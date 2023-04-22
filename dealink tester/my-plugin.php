<?php
/**
 * Plugin Name: My Plugin
 * Description: A plugin that supports a python script to run daily.
 * Version: 1.0
 * Author: muvap
 * Author URI: https://gptfu.com/
 */

function run_my_script() {
    $output = shell_exec('');//path to the python script main.py
    // Do something with the output, or just ignore it
}

// Hook the function to a WordPress action
add_action('my_plugin_daily_event', 'run_my_script');

// Schedule the event to run once a day
if (!wp_next_scheduled('my_plugin_daily_event')) {
    wp_schedule_event(time(), 'daily', 'my_plugin_daily_event');
}
