from flask import Flask, jsonify, request
from sqlite3 import connect as sqlite_connect
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return sqlite_connect('artdatabase.db')

@app.route('/artobjects/', methods=['GET'])
def get_art_objects():
    try:
        query = request.args.get('query', '')  # Get the query parameter
        conn = get_db_connection()
        cur = conn.cursor()

        if query:
            search_query = f"%{query}%"
            cur.execute("""
                SELECT * FROM t_art_objects 
                WHERE ArtObject LIKE ?
                OR ArtObjectLabel LIKE ?
                OR ArtObjectDescription LIKE ?
                OR ArtistLabel LIKE ?
                """, (search_query, search_query, search_query, search_query))
        else:
            cur.execute('SELECT * FROM t_art_objects')

        art_objects = cur.fetchall()
        cur.close()
        conn.close()

        if art_objects:
            art_objects_list = [dict(zip([column[0] for column in cur.description], ao)) for ao in art_objects]
            return jsonify(art_objects_list)
        else:
            return jsonify({"error": "No art objects found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/artobjects/<art_object_id>', methods=['GET'])
def get_individual_art_object(art_object_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM t_art_objects WHERE ArtObject = ?', (art_object_id,))
        art_object = cur.fetchone()
        cur.close()
        conn.close()

        if art_object:
            # Convert the row to a dictionary using column names from cur.description
            art_object_dict = dict(zip([column[0] for column in cur.description], art_object))
            return jsonify(art_object_dict)
        else:
            return jsonify({"error": "Art object not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/ownerships/<art_object_id>', methods=['GET'])
def get_ownerships(art_object_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM t_art_owners WHERE ArtObject = ?', (art_object_id,))
        ownerships = cur.fetchall()
        cur.close()
        conn.close()

        if ownerships:
            ownerships_list = [dict(zip([column[0] for column in cur.description], ownership)) for ownership in ownerships]
            return jsonify(ownerships_list)
        else:
            return jsonify({"error": "No ownerships found for the specified art object"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)