"""Prevent secret disclosure without damaging the dates needed for extraction."""
import pytest

from app.services.privacy import scrub


@pytest.mark.parametrize('text,secret', [
    ('您的验证码是 482913', '482913'),
    ('请输入验证码482913后继续', '482913'),
    ('验证码：482913', '482913'),
    ('Your verification code is 482913', '482913'),
    ('One-time passcode: 48291357', '48291357'),
    ('OTP 1234', '1234'),
    ('Call 6123 4567', '6123 4567'),
    ('Phone: 8123-4567', '8123-4567'),
    ('Contact +65 9123 4567', '9123 4567'),
])
def test_codes_and_local_phone_numbers_are_removed(text, secret):
    result = scrub(text)
    assert secret not in result
    assert 'REMOVED]' in result


@pytest.mark.parametrize('text', [
    'Due 2026-11-15 at 23:50',
    'Deadline: 15/11/2026',
    'Exam 15.11.2026, 09:00-10:15',
    'CS 4310 Assignment 2 is due on 15 November 2026.',
])
def test_dates_times_and_course_numbers_survive(text):
    assert scrub(text) == text
