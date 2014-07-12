require 'sqlite3'

class ResponseCache

  def initialize(path = "data/osm/cache.db")
    @db = SQLite3::Database.new path
    db.execute <<-SQL rescue nil
      create table cache (
        name text PRIMARY KEY,
        url text NOT NULL,
        response text NOT NULL
      );
    SQL
  end

  def fetch(name, url)
    name = name.downcase.strip
    db.execute("select response from cache where name = ?", name) do |row|
      return row.first
    end
    sleep 1 # Don't hammer them!
    resp = RestClient.get url
    db.execute "insert into cache values ( ?, ?, ? )", [name, url, resp]
    resp
  end

  private

  attr_reader :db
end
