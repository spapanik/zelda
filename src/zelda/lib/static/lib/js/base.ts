// eslint-disable-next-line @typescript-eslint/no-unused-vars
function saveMaxedOutPreference(that): void {
    const isChecked = that.checked;
    const maxAge = 60 * 60 * 24 * 365;
    document.cookie = `hideMaxedOut=${isChecked}; max-age=${maxAge}; path=/`;
    location.reload();
}
