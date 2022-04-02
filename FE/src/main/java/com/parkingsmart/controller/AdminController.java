package com.parkingsmart.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class AdminController {

	@GetMapping("/admin/home")
	public String getAdminHome() {
		return "admin/index";
	}
	
	@GetMapping("/admin/list-member")
	public String getAdminMember() {
		return "admin/table";
	}
	
	@GetMapping("/admin/profile")
	public String getProfile() {
		return "admin/profile";
	}
	
	@GetMapping("/admin/statistics")
	public String getStatistics() {
		return "admin/statistic";
	}
	
}
