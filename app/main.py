from flask import Flask, jsonify, request, abort
from flask_restful import reqparse, Api, Resource

from utils import check_datetime_format, convert_time_range
from db_requests import DBRequests
from settings import DAY, URL, TABLE_NAME, FORMATS

web_app = Flask(__name__)
db = DBRequests(URL, TABLE_NAME)


@web_app.route("/hello")
def hello():
    return "HELLO"


@web_app.route("/average_time", methods=["GET"])
def average_time():
    date = request.args.get("date")
    if check_datetime_format(DAY, date):
        return jsonify(
            {"average_time": f"{round(db.get_avg_queries_time_per_day(date), 2)}"}
        )
    abort(
        400,
        f"Hint: Check your time format. It should be {DAY}. Hint 2: parameter name is day",
    )


@web_app.route("/rows_per_thread", methods=["GET"])
def rows_per_thread():
    time_start, time_end = convert_time_range(
        [request.args.get("time_start"), request.args.get("time_end")]
    )

    if time_start is not None and time_start < time_end:
        response = db.get_avg_rows_per_thread(time_start, time_end)
        if response is not None:
            return jsonify({"rows_per_thread": f"{response}"})

    abort(
        400,
        f"Hint 1: Check your time format. It should be one of them: {FORMATS}. Hint 2: parameters names are time_start and time_end",
    )


@web_app.route("/rows_per_second", methods=["GET"])
def rows_per_second():
    time_start, time_end = convert_time_range(
        [request.args.get("time_start"), request.args.get("time_end")]
    )

    if time_start is not None and time_start < time_end:
        response = db.get_avg_rows_per_second(time_start, time_end)
        if response is not None:
            return jsonify({"rows_per_thread": f"{response}"})

    abort(
        400,
        f"Hint: Check your time format. It should be one of them: {FORMATS}. Hint 2: parameters names are time_start and time_end",
    )


@web_app.route("/threads_per_second", methods=["GET"])
def threads_per_second():

    time_start, time_end = convert_time_range(
        [request.args.get("time_start"), request.args.get("time_end")]
    )

    if time_start is not None and time_start < time_end:
        response = db.get_avg_threads_per_second(time_start, time_end)
        if response is not None:
            return jsonify({"rows_per_thread": f"{response}"})

    abort(
        400,
        f"Hint: Check your time format. It should be one of them: {FORMATS}. Hint 2: parameters names are time_start and time_end",
    )


if __name__ == "__main__":
    print(db.get_avg_queries_time_per_day("2019-10-18"))
    web_app.run(debug=True, host="0.0.0.0")
