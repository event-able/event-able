require 'sqlite3'

class ResponseCache

  def initialize(path = "data/osm/cache.db")
    @db = SQLite3::Database.new path
    db.execute <<-SQL rescue nil
      create table cache (
        key text PRIMARY KEY,
        value text NOT NULL
      );
    SQL
  end

  def fetch(key)
    name = key.downcase.strip
    db.execute("select value from cache where key = ?", key) do |row|
      return row.first
    end
    val = yield
    db.execute "insert into cache values ( ?, ? )", [key, val]
    val
  end

  private

  attr_reader :db
end
