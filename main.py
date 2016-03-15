def main():
    google_credentials = get_google_credentials()
    schedule = get_lectio_schedule()
    if schedule_has_changed(schedule, google_credentials):
        update_google_calendar_with_schedule(schedule, google_credentials)

if __name__ = "__main__":
    main()
