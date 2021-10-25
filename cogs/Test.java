@EventHandler
    public static void VillagerGUIClick(InventoryClickEvent event) {
        if(event.getCurrentItem() == null) return;
        if(event.getView().getTitle() == Strings.INV_NAME) {
            event.setCancelled(true);
            Player player = (Player) event.getWhoClicked();
            if(event.getCurrentItem().getItemMeta().hasDisplayName()) {
                switch (event.getCurrentItem().getItemMeta().getDisplayName()) {
                    case Strings.Close:
                        player.sendMessage(main.PREFIX + " §cClosed!");
                        player.closeInventory();
                        break;
                    case Strings.Fraction1:
                        for(UUID i : DataFile.fractionsTimer.keySet()) {
                            if(i.equals(player.getUniqueId())) {
                                LocalDateTime checkTime = DataFile.fractionsTimer.get(player.getUniqueId());
                                LocalDateTime checkNow = LocalDateTime.now();
                                if(checkNow.isBefore(checkTime)){
                                    Duration duration = Duration.between(checkNow, checkTime);
                                    player.sendMessage(main.PREFIX + "§cDu musst noch " + duration.toString() + "§cwarten!");
                                    return;
                                }
                            }
                        }
                        LocalDateTime now = LocalDateTime.now();
                        LocalDateTime now3 = now.plusSeconds(9);
                        Bukkit.getConsoleSender().sendMessage(now3.toString());
                        DataFile.fractionsTimer.put(player.getUniqueId(), now3);
                        player.sendMessage(main.PREFIX + " §aDu bist §bFraction 1 §abeigetreten!");
                        player.closeInventory();
                        break;
                    case Strings.Fraction2:
                        for(UUID i : DataFile.fractionsTimer.keySet()) {
                            if(i.equals(player.getUniqueId())) {
                                LocalDateTime checkTime = DataFile.fractionsTimer.get(player.getUniqueId());
                                LocalDateTime checkNow = LocalDateTime.now();
                                if(checkNow.isBefore(checkTime)){
                                    Duration duration = Duration.between(checkNow, checkTime);
                                    player.sendMessage(main.PREFIX + "§cDu musst noch " + duration.toString() + "§cwarten!");
                                    return;
                                }
                            }
                        }
                        LocalDateTime now2 = LocalDateTime.now();
                        LocalDateTime now4 = now2.plusSeconds(9);
                        DataFile.fractionsTimer.put(player.getUniqueId(), now4);
                        player.sendMessage(main.PREFIX + " §aDu bist §bFraction 2 §abeigetreten!");
                        player.closeInventory();
                        break;
                }
            }
            }else {
            Bukkit.getConsoleSender().sendMessage(main.PREFIX + "§4Finn §bstinkt!");
        }
    }