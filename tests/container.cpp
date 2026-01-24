#include <string>
#include <unordered_map>
#include <memory>
#include <cassert>

class Base {
public:
  virtual ~Base() = default;
};

class Derived : public Base {
public:
  Derived(const std::string &name) : m_name{name} {}

  const std::string &getName() const { return m_name; }

private:
  std::string m_name;
};

std::unordered_map<std::string, std::unique_ptr<Base>>
    s_map{};

Base *var1 = nullptr;

    void
    triggerDump() {
  assert(false && "dump triggered");
}

int
main(int argc, char *argv[])
{
    s_map.emplace(std::make_pair("node1", std::make_unique<Derived>("node1")));
    s_map.emplace(std::make_pair("node2", std::make_unique<Derived>("node2")));

    var1 = new Derived("var1");

    triggerDump();
}